from datetime import datetime
from app.common.exceptions import NotFoundException, AppException


# 🔹 APPLY COUPON (Preview API)
async def apply_coupon(request, unit_of_work):
    async with unit_of_work as uow:

        trip = await uow.trip_repo.get_by_id(request.trip_id)

        if not trip:
            raise NotFoundException("Trip not found")

        total_amount = trip.amount * request.seats

        coupon = await uow.coupon_repo.get_by_code(request.coupon_code)

        if not coupon or not coupon.is_active:
            raise AppException(detail="Invalid coupon")

        if coupon.expiry_date and coupon.expiry_date < datetime.utcnow():
            raise AppException(detail="Coupon expired")

        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            raise AppException(detail="Coupon usage limit reached")

        if coupon.min_amount and total_amount < coupon.min_amount:
            raise AppException(detail="Minimum amount not met")

        # 💰 calculate discount
        if coupon.discount_type == "flat":
            discount = coupon.discount_value
        else:
            discount = (coupon.discount_value / 100) * total_amount

        final_amount = max(total_amount - discount, 0)

        return {
            "success": True,
            "data": {
                "original_amount": total_amount,
                "discount": discount,
                "final_amount": final_amount,
                "applied_coupon_code": coupon.code
            }
        }


# 🔹 BOOK TRIP (Final API)
async def book_trip(request, applied_coupon_code, current_user, unit_of_work):
    async with unit_of_work as uow:

        # 🔐 user
        user_id = (
            current_user.get("user_id")
            or current_user.get("id")
            or current_user.get("sub")
        )

        if not user_id:
            raise AppException(detail="Invalid user token")

        # 🚗 trip
        trip = await uow.trip_repo.get_trip_for_update(request.trip_id)

        if not trip:
            raise NotFoundException("Trip not found")

        if request.seats <= 0:
            raise AppException(detail="Seats must be greater than 0")

        if trip.available_seats < request.seats:
            raise AppException(status_code=400, detail="Not enough seats available")

        # 💰 base amount
        total_amount = trip.amount * request.seats

        discount_amount = 0
        coupon_applied = False
        coupon_code = None

        # 🎟️ APPLY COUPON (from applied_coupon_code)
        if applied_coupon_code:

            coupon = await uow.coupon_repo.get_by_code(applied_coupon_code)

            if not coupon or not coupon.is_active:
                raise AppException(detail="Invalid coupon")

            if coupon.expiry_date and coupon.expiry_date < datetime.utcnow():
                raise AppException(detail="Coupon expired")

            if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                raise AppException(detail="Coupon usage limit reached")

            if coupon.min_amount and total_amount < coupon.min_amount:
                raise AppException(detail="Minimum amount not met")

            # 💰 discount
            if coupon.discount_type == "flat":
                discount_amount = coupon.discount_value
            else:
                discount_amount = (coupon.discount_value / 100) * total_amount

            coupon_applied = True
            coupon_code = coupon.code

            # increment usage
            coupon.used_count += 1

        # 💵 final amount
        final_amount = max(total_amount - discount_amount, 0)

        # 🔻 reduce seats
        trip.available_seats -= request.seats

        # 📦 create booking
        booking = await uow.booking_repo.create({
            "user_id": user_id,
            "trip_id": request.trip_id,
            "seats_booked": request.seats,
            "total_amount": final_amount,
            "status": "booked",
            "transaction_id": request.transaction_id,
            "coupon_applied": coupon_applied,
            "coupon_code": coupon_code,
            "discount_amount": discount_amount
        })

        await uow.commit()

        return {
            "success": True,
            "message": "Booking successful",
            "data": {
                "booking_id": str(booking.id),
                "trip_id": request.trip_id,
                "seats_booked": request.seats,
                "remaining_seats": trip.available_seats,
                "total_amount": final_amount,
                "discount": discount_amount
            }
        }
async def get_my_bookings(current_user, unit_of_work):
    async with unit_of_work as uow:

        # 🔐 user
        user_id = (
            current_user.get("user_id")
            or current_user.get("id")
            or current_user.get("sub")
        )

        if not user_id:
            raise AppException(detail="Invalid user")

        # 📦 fetch bookings
        bookings = await uow.booking_repo.get_by_user(user_id)

        # 🧾 response
        return {
            "success": True,
            "data": [
                {
                    "booking_id": str(b.id),
                    "trip_id": str(b.trip_id),
                    "seats_booked": b.seats_booked,
                    "total_amount": b.total_amount,
                    "status": b.status,
                    "coupon_applied": b.coupon_applied,
                    "coupon_code": b.coupon_code,
                    "discount_amount": b.discount_amount,
                    "transaction_id": b.transaction_id,
                    "created_at": b.created_at
                }
                for b in bookings
            ]
        }
async def cancel_booking(booking_id, current_user, unit_of_work):
    async with unit_of_work as uow:

        # 🔐 user
        user_id = (
            current_user.get("user_id")
            or current_user.get("id")
            or current_user.get("sub")
        )

        if not user_id:
            raise AppException(status_code=400, detail="Invalid user")

        # 📦 get booking
        booking = await uow.booking_repo.get_by_id(booking_id)

        if not booking:
            raise NotFoundException("Booking not found")

        # 🔒 prevent cancelling others' booking
        if str(booking.user_id) != str(user_id):
            raise AppException(status_code=403, detail="Not allowed")

        # ❌ already cancelled
        if booking.status == "cancelled":
            raise AppException(status_code=400, detail="Booking already cancelled")

        # 🚗 get trip (lock row)
        trip = await uow.trip_repo.get_trip_for_update(booking.trip_id)

        # 🔁 restore seats
        trip.available_seats += booking.seats_booked

        # 🎟️ restore coupon usage (optional but correct)
        if booking.coupon_applied and booking.coupon_code:
            coupon = await uow.coupon_repo.get_by_code(booking.coupon_code)
            if coupon and coupon.used_count > 0:
                coupon.used_count -= 1

        # 🔄 update status
        booking.status = "cancelled"

        await uow.commit()

        return {
            "success": True,
            "message": "Booking cancelled successfully",
            "booking_id": str(booking_id)
        }
        
