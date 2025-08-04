import uuid
from ..core.database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"), nullable=False)
    product_id = Column(String(100), nullable=False)  # Product ID, using String for now, can be changed to ForeignKey later
    quantity = Column(Integer, nullable=False, default=1)
    # Can add price snapshot to avoid cart being affected by price changes
    price_snapshot = Column(String(20), nullable=True)  # Store price as string to avoid floating point issues
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relationships
    cart = relationship("Cart", back_populates="items")
