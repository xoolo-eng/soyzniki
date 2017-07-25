def count_page(count_data, count_elements):
    '''
    count_page - функция для определения количества страниц,
    принимает количество зарисей, максимальное количество
    элументов на одной странице, тип данных - int
    '''
    from math import ceil
    if count_data % count_elements > 0:
        return ceil(count_data / count_elements)
    else:
        return count_data // count_elements


def get_html_pages(current_page, count_pages, link):
    '''
    принимает текущую станицу и общее количество страниц,
    возвращает список li > a
    '''
    template_pages = '<li {0}><a href="{2}{1}/">{1}</a></li>'
    pages = []
    for line in range(1, count_pages + 1):
        if line == current_page:
            pages.append(template_pages.format('class="active"', line, link))
        else:
            pages.append(template_pages.format('', line, link))
    return pages
