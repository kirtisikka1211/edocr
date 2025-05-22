from sqlalchemy import Column, String, Integer, ForeignKey, Text, LargeBinary,JSON
from sqlalchemy.orm import relationship
from db import Base

class PDF(Base):
    __tablename__ = "pdfs"

    pdf_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    pdf_file = Column(LargeBinary)

    drawings = relationship("Drawing", back_populates="pdf", cascade="all, delete-orphan")


class Drawing(Base):
    __tablename__ = "drawings"

    page_id = Column(String, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey("pdfs.pdf_id"), nullable=False)


    productNumber = Column(String)
    productFamily = Column(String)
    drawingNumber = Column(String)
    engineerName = Column(String)
    revision = Column(String)
    approvalDate = Column(String)
    status = Column(String)

    pdf = relationship("PDF", back_populates="drawings")
    notes = relationship("Note", back_populates="drawing", cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    page_id = Column(String, ForeignKey("drawings.page_id"), nullable=False)
    noteText = Column(JSON)  # Store full note list as JSON array

   

    drawing = relationship("Drawing", back_populates="notes")
