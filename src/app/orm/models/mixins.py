


# class CommonMixin:
#     name: Mapped[str] = mapped_column(String(255), nullable=True)
#     mobile_number: Mapped[str] = mapped_column(String(25), unique=True,nullable=False)
#     email: Mapped[str] = mapped_column(String(254), nullable=True)
#     alternative_mobile_number: Mapped[str] = mapped_column(String(25), nullable=True)
#     profile_pic: Mapped[str] = mapped_column(String(500), nullable=True)
#     gender: Mapped[str] = mapped_column(String(20), nullable=True)
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now(), nullable=False
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         onupdate=func.now(),
#         nullable=False,
#     )
    
#     role: Mapped[str] = mapped_column(String(50), nullable=False)
#     devices = relationship("UserDevice", back_populates="user")
