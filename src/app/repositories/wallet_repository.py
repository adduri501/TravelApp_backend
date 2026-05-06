from sqlalchemy import select
from app.orm.models.wallet_model import WalletTable

class WalletRepository:

    def __init__(self, session):
        self.session = session

    async def get_wallet(self, user_id):
        stmt = select(WalletTable).where(WalletTable.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def add_balance(self, user_id, amount):
        wallet = await self.get_wallet(user_id)

        if not wallet:
            wallet = WalletTable(user_id=user_id, balance=0)
            self.session.add(wallet)

        wallet.balance += amount