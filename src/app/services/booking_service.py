from datetime import datetime
from app.common.exceptions import NotFoundException, AppException


# 🔹 APPLY COUPON (Preview API)
async def apply_coupon(request, current_user, unit_of_work):
    async with unit_of_work as uow:

        # 🔐 user
        user_id = (
            current_user.get("user_id")
            or current_user.get("id")
            or current_user.get("sub")
        )
        print("USER FROM TOKEN:", user_id)
       

        total_bookings = await uow.booking_repo.count_user_successful_bookings(user_id)

        print("TOTAL BOOKINGS:", total_bookings)
        
        if not user_id:
            raise AppException(status_code=400, detail="Invalid user")

        trip = await uow.trip_repo.get_by_id(request.trip_id)

        if not trip:
            raise NotFoundException("Trip not found")

        total_amount = trip.amount * request.seats

        coupon = await uow.coupon_repo.get_by_code(request.coupon_code)
        print("IS FIRST TIME:", coupon.is_first_time_only)

        if not coupon or not coupon.is_active:
            raise AppException(status_code=400, detail="This coupon doesn’t exist… or it’s playing hide and seek 🙈")

        # ✅ CHECK HERE (moved from booking)
        already_used = await uow.booking_repo.has_used_coupon(
            user_id, request.coupon_code
        )

        if already_used:
            raise AppException(
                status_code=400,
                detail="This coupon is loyal—it only works once per person 😄"
            )

        if coupon.coupon_type == "FIRST":
            total_bookings = await uow.booking_repo.count_user_successful_bookings(user_id)

            if total_bookings > 0:
                raise AppException(
                    status_code=400,
                    detail="You’re no longer a beginner 😄 This coupon is only for first-timers."
                )

        # existing validations
        if coupon.expiry_date and coupon.expiry_date < datetime.utcnow():
            raise AppException(status_code=400, detail="Too late 😅 This coupon has already retired")

        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            raise AppException(status_code=400, detail="All gone! This coupon sold out faster than concert tickets 🎟️")

        if coupon.min_amount and total_amount < coupon.min_amount:
            raise AppException(status_code=400, detail="Your cart is shy—add a little more to impress this coupon 😉")

        # 💰 calculate discount
        if coupon.discount_type == "flat":
            discount = coupon.discount_value

        elif coupon.discount_type == "percentage":
            discount = (coupon.discount_value / 100) * total_amount

        else:
            raise AppException(
                status_code=400,
                detail="Invalid coupon type 🤔"
            )

        # safety
        discount = min(discount, total_amount)
        discount = round(discount, 2)

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

        user_id = (
             current_user.get("user_id")
              or current_user.get("id")
                or current_user.get("sub")
        )

        if not user_id:
            raise AppException(status_code=400, detail="Invalid user token")

        trip = await uow.trip_repo.get_trip_for_update(request.trip_id)

        if not trip:
            raise NotFoundException("Trip not found")

        if request.seats <= 0:
            raise AppException(status_code=400, detail="Seats must be greater than 0")

        if trip.available_seats < request.seats:
            raise AppException(status_code=400, detail="Not enough seats available")

        total_amount = trip.amount * request.seats

        discount_amount = 0
        coupon_applied = False
        coupon_code = None

        if applied_coupon_code:

            coupon = await uow.coupon_repo.get_by_code(applied_coupon_code)

            if not coupon or not coupon.is_active:
                raise AppException(status_code=400, detail="Invalid coupon")

            if coupon.expiry_date and coupon.expiry_date < datetime.utcnow():
                raise AppException(status_code=400, detail="Coupon expired")

            if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                raise AppException(status_code=400, detail="Coupon usage limit reached")

            if coupon.min_amount and total_amount < coupon.min_amount:
                raise AppException(status_code=400, detail="Minimum amount not met")

            # 🔁 KEEP VALIDATION (security)
            already_used = await uow.booking_repo.has_used_coupon(
                user_id, applied_coupon_code
            )

            if already_used:
                raise AppException(
                    status_code=400,
                    detail="This coupon is loyal—it only works once per person 😄"
                )

            if coupon.is_first_time_only:
                total_bookings = await uow.booking_repo.count_user_successful_bookings(user_id)

                if total_bookings > 0:
                    raise AppException(
                        status_code=400,
                        detail="You’re no longer a beginner 😄 This coupon is only for first-timers."
                    )

        

        coupon_applied = True
        coupon_code = coupon.code

        coupon.used_count += 1
    if request.use_wallet:
        wallet = await uow.wallet_repo.get_wallet(user_id)

        if wallet and wallet.balance > 0:
            deduction = min(wallet.balance, total_amount)

            wallet.balance -= deduction
            total_amount -= deduction

        final_amount = max(total_amount - discount_amount, 0)

        trip.available_seats -= request.seats

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
        user = await uow.user_repo.get_by_id(user_id)

        if user.referred_by:
                referrer = await uow.user_repo.get_by_referral_code(user.referred_by)

                if referrer:
                    await uow.wallet_repo.add_balance(referrer.id, 50)
                    await uow.wallet_repo.add_balance(user_id, 50)

                    user.referred_by = None

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

        user_id = (
            current_user.get("user_id")
            or current_user.get("id")
            or current_user.get("sub")
        )

        if not user_id:
            raise AppException(status_code=400, detail="Invalid user")

        bookings = await uow.booking_repo.get_by_user(user_id)

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

        # 🚗 lock trip row
        trip = await uow.trip_repo.get_trip_for_update(booking.trip_id)

        # 🔁 restore seats
        trip.available_seats += booking.seats_booked

        # 🎟️ restore coupon usage
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

async def get_available_coupons(current_user, unit_of_work):
    async with unit_of_work as uow:

        user_id = current_user.get("id")

        total_bookings = await uow.booking_repo.count_user_successful_bookings(user_id)

        coupons = await uow.coupon_repo.get_all()

        result = []

        for c in coupons:

            if not c.is_active:
                continue

            if c.coupon_type == "FIRST" and total_bookings > 0:
                continue

            result.append({
                "code": c.code,
                "type": c.coupon_type,
                "discount": c.discount_value
            })

        return {"success": True, "data": result}