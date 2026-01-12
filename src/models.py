from __future__ import annotations
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    # Padre
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    following: Mapped[List["Follower"]] = relationship(foreign_keys="Follower.user_from_id", back_populates="user_from")
    followers: Mapped[List["Follower"]] = relationship(foreign_keys="Follower.user_to_id", back_populates="user_to")
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password,
        }


class Post(db.Model):
    __tablename__ = "post"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    enlace: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Hijo
    user: Mapped["User"] = relationship(back_populates="posts")

    # Padre
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    medias: Mapped[List["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "enlace": self.enlace,
            "user_id": self.user_id
        }


class Comment(db.Model):
    __tablename__ = "comment"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    # Hijo
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }


class Media(db.Model):
    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    # Hijo
    post: Mapped["Post"] = relationship(back_populates="medias")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }


class Follower(db.Model):
    __tablename__ = "follower"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # Hijo
    user_from: Mapped["User"] = relationship(foreign_keys=[user_from_id], back_populates="following")
    user_to: Mapped["User"] = relationship(foreign_keys=[user_to_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
   
