import uuid
import logging

from pyrogram.enums import ParseMode
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent)

from test_tele.features.extractors.manga import *
from test_tele.features.pyrogram.utils import not_found_msg, QUERY

db = QUERY

async def image_keyboard(my_list: dict, inline_text = None) -> InlineKeyboardMarkup:
    optional_button = None
    row2_button = None
    query = None
    if 'manga_url' in my_list:
        button_name = 'Select Chapter 📚'
        see_chapter = my_list['manga_url'].split("-")
        row2_button = [
            InlineKeyboardButton('🔄', switch_inline_query_current_chat=inline_text)
        ]
    elif 'doujin_url' in my_list:
        button_name = 'Read This 📕'
        see_chapter = ['.md', f"code:{my_list['code']}"]
        row2_button = [
            InlineKeyboardButton('🔄', switch_inline_query_current_chat=inline_text)
        ]
    elif 'chapter' in my_list:
        button_name = 'Start Reading 📖'
        see_chapter = my_list['link_chapter'].split("-")
    elif 'images' in my_list:
        button_name = '◀️'
        see_chapter = my_list['prev_ch'].split("-")
        optional_button = InlineKeyboardButton('▶️', switch_inline_query_current_chat=my_list['next_ch'].replace("-", " "))
    
    query = ' '.join(see_chapter)
    buttons = [[
                InlineKeyboardButton(button_name,
                                    switch_inline_query_current_chat=query)
            ]] 
    
    if row2_button is not None:
        buttons.append(row2_button)
    if optional_button is not None:
        buttons[0].append(optional_button)

    return InlineKeyboardMarkup(buttons)


async def create_query_result(my_list, query, doujin=False, lists=[]):
    if not doujin:
        if '-r18' in query:
            input_message_content=InputTextMessageContent(
                f"**{my_list['title']}**\n"
                f"Code : {my_list['code']}\n"
                f"Category : {my_list['category']}\n",
                # f"Initiating synchronization, please wait...",
                parse_mode=ParseMode.MARKDOWN
            )
            desc = f"Code : {my_list['code']}\nCategory : {my_list['category']}"
        else:
            input_message_content=InputTextMessageContent(
                f"**{my_list['title']}**\n"
                f"Author : {my_list['author']}\n"
                f"Rating : {my_list['rating']}\n"
                f"Genres : {my_list['genres']}\n",
                parse_mode=ParseMode.MARKDOWN
            )
            desc = f"Author : {my_list['author']}\nRating : {my_list['rating']}"

        result = InlineQueryResultArticle(
            title=my_list['title'],
            input_message_content=input_message_content,
            id=str(uuid.uuid4()),
            # url=my_list['manga_url'],
            description=desc,
            thumb_url=my_list['thumbnail'],
            reply_markup=await image_keyboard(my_list, query)
        )
        return result
    else:
        result = InlineQueryResultPhoto(
            photo_url=my_list['url'],
            id=str(uuid.uuid4()),
            caption=(
                f"**{lists[-1]['title']}**\n"
                f"Artist : {lists[-1]['artist']}\n"
                f"Languange : {lists[-1]['language']}\n"
                f"Tags : {lists[-1]['tags']}"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        return result


async def inline_mangapark(client, inline_query):
    """Show Mangapark arts"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0
    doujin = False

    if '-r18' in query:
        lists = await get_doujin_list(query, pid)
    elif 'code:' in query:
        query = query.replace(".md code:", "").strip()
        lists = await get_img_list_gellerydl(query, pid) # masih ada error : IndexError: list index out of range
        doujin = True
    else:
        lang = db.read_datas('settings', ['lang'], 'chat_id = %s', [inline_query.from_user.id])
        if lang:
            lists = await get_manga_list(query, pid, lang[0][0])
        else:
            lists = await get_manga_list(query, pid)

    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)
         
    try:
        if not lists:
            return
        elif doujin and lists:
            all_list = lists[-1]['img_urls'] # masih ada error : KeyError: 'img_urls'
        elif not doujin and lists: 
            all_list = lists
        
        for my_list in all_list:
            result = await create_query_result(my_list, query, doujin, lists)
            if result:
                results.append(result)

        await client.answer_inline_query(
            inline_query.id,
            results=results,
            cache_time=0,
            is_gallery=False if not doujin else True, 
            next_offset=str(pid + OFFSET_PID)
        )
    except Exception as err:
        logging.error(err, exc_info=True)


async def check_inline_query_type(client, inline_query):
    query = inline_query.query

    if not query:
        return
    
    if query.count('/') > 1:
        return await inline_chapter_images(client, inline_query)
    
    return await inline_chapter_list(client, inline_query)


async def inline_chapter_list(client, inline_query):
    query = inline_query.query
    offset = inline_query.offset
    pid = int(offset) if offset else 0

    link = query.replace(" ", "-")
    lists = await get_chapter_list(link, pid)

    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)
         
    if lists:
        try:
            for my_list in lists:
                result = InlineQueryResultArticle(
                    title=my_list['title'],
                    input_message_content=InputTextMessageContent(
                        f"**{my_list['title']}**\n"
                        f"Chapter : {my_list['chapter']}\n",
                        parse_mode=ParseMode.MARKDOWN
                    ),
                    id=str(uuid.uuid4()),
                    # url=my_list['manga_url'],
                    description=f"Chapter : {my_list['chapter']}",
                    reply_markup=await image_keyboard(my_list),
                )
                results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=0,
                next_offset=str(pid + OFFSET)
            )
        except Exception as err:
            logging.error(err, exc_info=True)


async def inline_chapter_images(client, inline_query):
    query = inline_query.query
    offset = inline_query.offset
    pid = int(offset) if offset else 0
    link = query.replace(" ", "-")
    lists = await get_chapter_images(link, pid)

    results = []
    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)
         
    if lists:
        try:
            for my_list in lists:
                result = InlineQueryResultPhoto(
                    photo_url=my_list['images'],
                    id=str(uuid.uuid4()),
                    reply_markup=await image_keyboard(my_list),
                )
                results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=0,
                is_gallery=True,
                next_offset=str(pid + OFFSET)
            )
        except Exception as err:
            logging.error(err, exc_info=True)


async def get_manga_cover(url):
    return await get_manga_file(url)



# async def download_chapter_images(client, inline_query):
#     query = inline_query.query
#     offset = inline_query.offset
#     pid = int(offset) if offset else 0
#     link = query.replace(" ", "-")
#     lists = await get_chapter_images(link, pid)

#     results = []
#     if pid == 0 and not lists:
#         return await not_found_msg(client, inline_query)
         
#     if lists:
#         try:
#             for my_list in lists:
#                 result = InlineQueryResultPhoto(
#                     photo_url=my_list['images'],
#                     id=str(uuid.uuid4()),
#                     reply_markup=await image_keyboard(my_list),
#                 )
#                 results.append(result)
    
#             await client.answer_inline_query(
#                 inline_query.id,
#                 results=results,
#                 cache_time=0,
#                 is_gallery=True,
#                 next_offset=str(pid + OFFSET)
#             )
#         except Exception as err:
#             logging.error(err, exc_info=True)
