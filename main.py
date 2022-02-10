# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import time


HEADER = """<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
	<script src="scripts.js"></script>
	<style>
		.block {
			position: relative;
		}

		/* Оформление скрытого элемента по умолчанию */
		.hidden {
			display: none;
			position: absolute;
			bottom: 130%;
			left: 0px;
			background-color: #fff;
			color: #3aaeda;
			padding: 5px;
			text-align: center;
			-moz-box-shadow: 0 1px 1px rgba(0, 0, 0, .16);
			-webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, .16);
			box-shadow: 0 1px 1px rgba(0, 0, 0, .16);
			font-size: 12px;
		}

		/* Дополнительное оформление скрытого элемента(необязательно) */
		.focus+.hidden:before {
			content: " ";
			position: absolute;
			top: 98%;
			left: 10%;
			margin-left: -5px;
			border-width: 5px;
			border-style: solid;
			height: 0;
			width: 0;
			border: 7px solid transparent;
			border-right: 7px solid #fff;
			border-color: #fff transparent transparent transparent;
			z-index: 2;
		}

		/* Дополнительное оформление скрытого элемента(необязательно) */
		.focus+.hidden:after {
			content: " ";
			position: absolute;
			top: 100%;
			left: 10%;
			margin-left: -5px;
			border-width: 5px;
			border-style: solid;
			height: 0;
			width: 0;
			border: 7px solid transparent;
			border-right: 7px solid #fff;
			border-color: rgba(0, 0, 0, .16) transparent transparent transparent;
			z-index: 1;
		}

		/* Появление скрытого элемента при клике */
		.focus:focus+.hidden {
			display: block;
		}
		a{
      text-decoration: none;
      color: #000;
    }
	</style>
</head>\n"""

def extract_data_from_report3(filename):
    soup = BeautifulSoup(open(filename, encoding='utf-8'), "lxml")
    print(soup.text)


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    out = []
    for i in range(len(string)):
        c = string[i]
        if c == '(':
            # добавляем в стак индексы всех попавшихся открывающихся скобок
            stack.append(i)
        elif c == ')' and stack:
            # если попалась закрывающая скобка, то убираем индекс последней открывающей скобки
            start = stack.pop()
            level = len(stack)
            from1 = string[start + 1]
            to1 = string[i - 1]
            out.append((level, string[start + 1: i]))
    return out


def get_text_str():
    with open("ya_zapechatayu_nebesa_fb2_texts.txt", "r", encoding="utf-8") as f:
        return f.read()


def get_title_str():
    with open("ya_zapechatayu_nebesa_fb2_tiltles.txt", "r", encoding="utf-8") as f:
        return f.read()


def get_text():
    """Берет текст между двумя указанными тегами, но только если нет вложенности и теги последовательны"""
    t1 = time.time()
    string = get_title_str()
    print("Время работы get_title_str", time.time() - t1)
    out = []
    indexes_end = [m.start() for m in re.finditer('</title>', string)]
    indexes_start = [m.start() for m in re.finditer('<title>', string)]
    for i in range(len(indexes_end) - 1):
        elem = indexes_end[i]
        out.append(string[indexes_end[i]:indexes_start[i + 1]])
    print("Время работы get_titles", time.time() - t1)
    return out

    return out


def get_titles():
    t1 = time.time()
    """Generate parenthesized contents in string as pairs (level, contents)."""
    string = get_title_str()
    print("Время работы get_title_str", time.time() - t1)
    out = []
    indexes_end = [m.start() for m in re.finditer('</title>', string)]
    indexes_start = [m.start() for m in re.finditer('<title>', string)]
    for i in range(len(indexes_end)):
        elem = indexes_end[i]
        out.append(string[indexes_start[i] + 7:indexes_end[i]])
    print("Время работы get_titles", time.time() - t1)
    return out


def get_clear_texts():
    a = get_text()
    a = [i.replace("\n</section><section>\n", "") for i in a]
    return a


def get_clear_titles():
    a = get_titles()
    a = [i for i in a]
    return a


def get_double_list():
    out = []
    for title, text in zip(get_clear_titles(), get_clear_texts()):
        out.append([title, text])
    return out


def beauty_print(l):
    for i in l:
        print(i)


def create_file_and_write(file, string):
    with open(file, mode="w", encoding="utf-8") as f:
        f.write(string)


# beauty_print(get_double_list())

def place_new_text(text, describtion):  #
    out = f"""<nobr class="block"> <a href="#" class="focus">{text}</a> <span class="hidden">{describtion} </span> </nobr>"""
    return out


# out = f'<nobr id="numOfPlaces"></nobr>'

def create_html():
    bad_symbols = '/\\:*?"<>|'
    t2 = time.time()
    a = get_double_list()
    print("Время работы всего", time.time() - t2)
    number = 1
    for i in a:
        string = ""
        string += HEADER
        title, text = i
        if "Глава 647" in title:
            print(123)
        string += f"\n<a name=t{number}></a><h3 class=book>\n{title}<br/></h3>{text}\n"
        string = replace_old_text("Мэн Хао", "Главный герой", string)
        string = replace_old_text("Юньцзе", "Уезд (дом гг)", string)
        string = replace_old_text(set(["Государство Чжао",
                                   "Государства Чжао",
                                   "Государству Чжао",
                                   "Государство Чжао",
                                   "Государством Чжао",
                                   "Государству Чжао",
                                   "Государству Чжао",
                                   ]), "Страна гг", string)
        title = "".join(e for e in title if e not in bad_symbols)
        create_file_and_write(f"{title.replace(r'<p>', '').replace(r'</p>', '')}.html", string)
        number += 1
    return string

def replace_with_no_sens(where, what, to):
    insensitive_hippo = re.compile(re.escape(what), re.IGNORECASE)
    return insensitive_hippo.sub(to, where)

def replace_old_text(old: str or list or set, new: str, big_text: str):
    if isinstance(old, str):
        # создаем новую вставку с ссылкой
        text = place_new_text(old, new)
        # изменяем основной текст
        big_text = big_text.replace(old, text)
    elif isinstance(old, (list, set)):
        for i in old:
            # создаем новую вставку с ссылкой
            text = place_new_text(i, new)
            # изменяем основной текст
            # big_text = big_text.replace(i, text)
            big_text = replace_with_no_sens(big_text, i, text)
    return big_text


create_html()

# extract_data_from_report3("ya_zapechatayu_nebesa1.fb2")
