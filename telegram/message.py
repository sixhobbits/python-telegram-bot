#!/usr/bin/env python
# pylint: disable=R0902,R0912,R0913
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2016
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains a object that represents a Telegram Message."""

import sys
from datetime import datetime
from time import mktime

from telegram import (Audio, Contact, Document, Chat, Location, PhotoSize, Sticker, TelegramObject,
                      User, Video, Voice, Venue, MessageEntity)


class Message(TelegramObject):
    """This object represents a Telegram Message.

    Note:
        * In Python `from` is a reserved word, use `from_user` instead.

    Attributes:
        message_id (int):
        from_user (:class:`telegram.User`):
        date (:class:`datetime.datetime`):
        forward_from (:class:`telegram.User`):
        forward_from_chat (:class:`telegram.Chat`):
        forward_date (:class:`datetime.datetime`):
        reply_to_message (:class:`telegram.Message`):
        edit_date (:class:`datetime.datetime`):
        text (str):
        audio (:class:`telegram.Audio`):
        document (:class:`telegram.Document`):
        photo (List[:class:`telegram.PhotoSize`]):
        sticker (:class:`telegram.Sticker`):
        video (:class:`telegram.Video`):
        voice (:class:`telegram.Voice`):
        caption (str):
        contact (:class:`telegram.Contact`):
        location (:class:`telegram.Location`):
        new_chat_member (:class:`telegram.User`):
        left_chat_member (:class:`telegram.User`):
        new_chat_title (str):
        new_chat_photo (List[:class:`telegram.PhotoSize`]):
        delete_chat_photo (bool):
        group_chat_created (bool):
        supergroup_chat_created (bool):
        migrate_to_chat_id (int):
        migrate_from_chat_id (int):
        channel_chat_created (bool):

    Deprecated: 4.0
        new_chat_participant (:class:`telegram.User`): Use `new_chat_member`
        instead.

        left_chat_participant  (:class:`telegram.User`): Use `left_chat_member`
        instead.

    Args:
        message_id (int):
        from_user (:class:`telegram.User`):
        date (:class:`datetime.datetime`):
        chat (:class:`telegram.Chat`):
        **kwargs: Arbitrary keyword arguments.

    Keyword Args:
        forward_from (Optional[:class:`telegram.User`]):
        forward_from_chat (:class:`telegram.Chat`):
        forward_date (Optional[:class:`datetime.datetime`]):
        reply_to_message (Optional[:class:`telegram.Message`]):
        edit_date (Optional[:class:`datetime.datetime`]):
        text (Optional[str]):
        audio (Optional[:class:`telegram.Audio`]):
        document (Optional[:class:`telegram.Document`]):
        photo (Optional[List[:class:`telegram.PhotoSize`]]):
        sticker (Optional[:class:`telegram.Sticker`]):
        video (Optional[:class:`telegram.Video`]):
        voice (Optional[:class:`telegram.Voice`]):
        caption (Optional[str]):
        contact (Optional[:class:`telegram.Contact`]):
        location (Optional[:class:`telegram.Location`]):
        new_chat_member (Optional[:class:`telegram.User`]):
        left_chat_member (Optional[:class:`telegram.User`]):
        new_chat_title (Optional[str]):
        new_chat_photo (Optional[List[:class:`telegram.PhotoSize`]):
        delete_chat_photo (Optional[bool]):
        group_chat_created (Optional[bool]):
        supergroup_chat_created (Optional[bool]):
        migrate_to_chat_id (Optional[int]):
        migrate_from_chat_id (Optional[int]):
        channel_chat_created (Optional[bool]):
        bot (Optional[Bot]): The Bot to use for instance methods
    """

    def __init__(self, message_id, from_user, date, chat, bot=None, **kwargs):
        # Required
        self.message_id = int(message_id)
        self.from_user = from_user
        self.date = date
        self.chat = chat
        # Optionals
        self.forward_from = kwargs.get('forward_from')
        self.forward_from_chat = kwargs.get('forward_from_chat')
        self.forward_date = kwargs.get('forward_date')
        self.reply_to_message = kwargs.get('reply_to_message')
        self.edit_date = kwargs.get('edit_date')
        self.text = kwargs.get('text', '')
        self.entities = kwargs.get('entities', list())
        self.audio = kwargs.get('audio')
        self.document = kwargs.get('document')
        self.photo = kwargs.get('photo')
        self.sticker = kwargs.get('sticker')
        self.video = kwargs.get('video')
        self.voice = kwargs.get('voice')
        self.caption = kwargs.get('caption', '')
        self.contact = kwargs.get('contact')
        self.location = kwargs.get('location')
        self.venue = kwargs.get('venue')
        self.new_chat_member = kwargs.get('new_chat_member')
        self.left_chat_member = kwargs.get('left_chat_member')
        self.new_chat_title = kwargs.get('new_chat_title', '')
        self.new_chat_photo = kwargs.get('new_chat_photo')
        self.delete_chat_photo = bool(kwargs.get('delete_chat_photo', False))
        self.group_chat_created = bool(kwargs.get('group_chat_created', False))
        self.supergroup_chat_created = bool(kwargs.get('supergroup_chat_created', False))
        self.migrate_to_chat_id = int(kwargs.get('migrate_to_chat_id', 0))
        self.migrate_from_chat_id = int(kwargs.get('migrate_from_chat_id', 0))
        self.channel_chat_created = bool(kwargs.get('channel_chat_created', False))
        self.pinned_message = kwargs.get('pinned_message')

        self.bot = bot

    @property
    def chat_id(self):
        """int: Short for :attr:`Message.chat.id`"""
        return self.chat.id

    @staticmethod
    def de_json(data, bot):
        """
        Args:
            data (dict):
            bot (telegram.Bot):

        Returns:
            telegram.Message:
        """
        if not data:
            return None

        data['from_user'] = User.de_json(data.get('from'), bot)
        data['date'] = datetime.fromtimestamp(data['date'])
        data['chat'] = Chat.de_json(data.get('chat'), bot)
        data['entities'] = MessageEntity.de_list(data.get('entities'), bot)
        data['forward_from'] = User.de_json(data.get('forward_from'), bot)
        data['forward_from_chat'] = Chat.de_json(data.get('forward_from_chat'), bot)
        data['forward_date'] = Message._fromtimestamp(data.get('forward_date'))
        data['reply_to_message'] = Message.de_json(data.get('reply_to_message'), bot)
        data['edit_date'] = Message._fromtimestamp(data.get('edit_date'))
        data['audio'] = Audio.de_json(data.get('audio'), bot)
        data['document'] = Document.de_json(data.get('document'), bot)
        data['photo'] = PhotoSize.de_list(data.get('photo'), bot)
        data['sticker'] = Sticker.de_json(data.get('sticker'), bot)
        data['video'] = Video.de_json(data.get('video'), bot)
        data['voice'] = Voice.de_json(data.get('voice'), bot)
        data['contact'] = Contact.de_json(data.get('contact'), bot)
        data['location'] = Location.de_json(data.get('location'), bot)
        data['venue'] = Venue.de_json(data.get('venue'), bot)
        data['new_chat_member'] = User.de_json(data.get('new_chat_member'), bot)
        data['left_chat_member'] = User.de_json(data.get('left_chat_member'), bot)
        data['new_chat_photo'] = PhotoSize.de_list(data.get('new_chat_photo'), bot)
        data['pinned_message'] = Message.de_json(data.get('pinned_message'), bot)

        return Message(bot=bot, **data)

    def __getitem__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        elif item == 'chat_id':
            return self.chat.id

    def to_dict(self):
        """
        Returns:
            dict:
        """
        data = super(Message, self).to_dict()

        # Required
        data['from'] = data.pop('from_user', None)
        data['date'] = self._totimestamp(self.date)
        # Optionals
        if self.forward_date:
            data['forward_date'] = self._totimestamp(self.forward_date)
        if self.edit_date:
            data['edit_date'] = self._totimestamp(self.edit_date)
        if self.photo:
            data['photo'] = [p.to_dict() for p in self.photo]
        if self.entities:
            data['entities'] = [e.to_dict() for e in self.entities]
        if self.new_chat_photo:
            data['new_chat_photo'] = [p.to_dict() for p in self.new_chat_photo]

        return data

    @staticmethod
    def _fromtimestamp(unixtime):
        """
        Args:
            unixtime (int):

        Returns:
            datetime.datetime:
        """
        if not unixtime:
            return None

        return datetime.fromtimestamp(unixtime)

    @staticmethod
    def _totimestamp(dt_obj):
        """
        Args:
            dt_obj (:class:`datetime.datetime`):

        Returns:
            int:
        """
        if not dt_obj:
            return None

        try:
            # Python 3.3+
            return int(dt_obj.timestamp())
        except AttributeError:
            # Python 3 (< 3.3) and Python 2
            return int(mktime(dt_obj.timetuple()))

    def reply_text(self, *args, **kwargs):
        """Shortcut for ``bot.sendMessage(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendMessage(self.chat_id, *args, **kwargs)

    def reply_photo(self, *args, **kwargs):
        """Shortcut for ``bot.sendPhoto(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendPhoto(self.chat_id, *args, **kwargs)

    def reply_audio(self, *args, **kwargs):
        """Shortcut for ``bot.sendAudio(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendAudio(self.chat_id, *args, **kwargs)

    def reply_document(self, *args, **kwargs):
        """Shortcut for ``bot.sendDocument(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendDocument(self.chat_id, *args, **kwargs)

    def reply_sticker(self, *args, **kwargs):
        """Shortcut for ``bot.sendSticker(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendSticker(self.chat_id, *args, **kwargs)

    def reply_video(self, *args, **kwargs):
        """Shortcut for ``bot.sendVideo(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendVideo(self.chat_id, *args, **kwargs)

    def reply_voice(self, *args, **kwargs):
        """Shortcut for ``bot.sendVoice(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendVoice(self.chat_id, *args, **kwargs)

    def reply_location(self, *args, **kwargs):
        """Shortcut for ``bot.sendLocation(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendLocation(self.chat_id, *args, **kwargs)

    def reply_venue(self, *args, **kwargs):
        """Shortcut for ``bot.sendVenue(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendVenue(self.chat_id, *args, **kwargs)

    def reply_contact(self, *args, **kwargs):
        """Shortcut for ``bot.sendContact(update.message.chat_id, *args, **kwargs)``"""
        return self.bot.sendContact(self.chat_id, *args, **kwargs)

    def forward(self, chat_id, disable_notification=False):
        """Shortcut for

            bot.forwardMessage(chat_id=chat_id,
                               from_chat_id=update.message.chat_id,
                               disable_notification=disable_notification,
                               message_id=update.message.message_id)

        """
        return self.bot.forwardMessage(
            chat_id=chat_id,
            from_chat_id=self.chat_id,
            disable_notification=disable_notification,
            message_id=self.message_id)

    def parse_entity(self, entity):
        """
        Returns the text from a given :class:`telegram.MessageEntity`.

        Note:
            This method is present because Telegram calculates the offset and length in
            UTF-16 codepoint pairs, which some versions of Python don't handle automatically.
            (That is, you can't just slice ``Message.text`` with the offset and length.)

        Args:
            entity (MessageEntity): The entity to extract the text from. It must be an entity that
                belongs to this message.

        Returns:
            str: The text of the given entity
        """
        # Is it a narrow build, if so we don't need to convert
        if sys.maxunicode == 0xffff:
            return self.text[entity.offset:entity.offset + entity.length]
        else:
            entity_text = self.text.encode('utf-16-le')
            entity_text = entity_text[entity.offset * 2:(entity.offset + entity.length) * 2]

        return entity_text.decode('utf-16-le')

    def parse_entities(self, types=None):
        """
        Returns a ``dict`` that maps :class:`telegram.MessageEntity` to ``str``.
        It contains entities from this message filtered by their ``type`` attribute as the key, and
        the text that each entity belongs to as the value of the ``dict``.

        Note:
            This method should always be used instead of the ``entities`` attribute, since it
            calculates the correct substring from the message text based on UTF-16 codepoints.
            See ``get_entity_text`` for more info.

        Args:
            types (Optional[list]): List of ``MessageEntity`` types as strings. If the ``type``
                attribute of an entity is contained in this list, it will be returned.
                Defaults to a list of all types. All types can be found as constants in
                :class:`telegram.MessageEntity`.

        Returns:
            dict[:class:`telegram.MessageEntity`, ``str``]: A dictionary of entities mapped to the
                text that belongs to them, calculated based on UTF-16 codepoints.
        """
        if types is None:
            types = MessageEntity.ALL_TYPES

        return {entity: self.parse_entity(entity)
                for entity in self.entities if entity.type in types}
