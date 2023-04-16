
from bs4 import BeautifulSoup, Tag, NavigableString
import request_test
import os

TARGET_SCRAPED_URL = os.getenv('TARGET_SCRAPED_URL')

def is_string(tag_str: str) -> bool:
    return isinstance(tag_str, NavigableString)

def get_elements_by_tag_name(url, tag: str, attrs: dict[str, str]) -> list[Tag]:
    response = request_test.get(url)
    bs = BeautifulSoup(response.content, 'html.parser')
    elements = bs.find_all(tag, attrs=attrs)
    return elements


def get_serihu_contents():
    serihu_elements = get_elements_by_tag_name(
        url=TARGET_SCRAPED_URL, tag='td', attrs={'class': 'serihu'})

    for serihu_element in serihu_elements:
        elements: list[Tag] = serihu_element.find_all('font')

        for element in elements:
            scraped_text = element.text

            if not "：" in scraped_text:
                continue

            speaker, content = scraped_text.split('：')

            if not speaker == '魔理沙':
                continue

            yield "," + content + "\n"


def read_csv():
    with open('apis/openai/gpt/tools/edit.csv', 'r') as f:
        r = f.read()

    return r

def write_to_output():
    with open('apis/openai/gpt/tools/edit.csv', 'a') as f:
        for content in get_serihu_contents():
            f.write(content)

def get_edit_contents():
    with open('apis/openai/gpt/tools/edit.csv', 'r') as f:
        contents = f.readlines()

    for content in contents:
        prompt, _ = content.split(',')

        if not prompt:
            continue

        yield content

def write_to_output() -> None:
    with open('apis/openai/gpt/tools/output.csv', 'w') as f:
        for content in get_edit_contents():
            f.write(content)

if __name__ == "__main__":
    write_to_output()
