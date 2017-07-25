var input = 'textarea'
var text_element = $(input).get();
var dock = document.createElement('div');
dock.className = 'dock';
var elements = {
    'alignment_left': 'main/icons_editor/alignment_left.svg',
    'alignment_right': 'main/icons_editor/alignment_right.svg',
    'alignment_center': 'main/icons_editor/alignment_center.svg',
    'alignment_justify': 'main/icons_editor/alignment_justify.svg',
    'link': 'main/icons_editor/link.svg',
    'heading_1': 'main/icons_editor/heading_1.svg',
    'heading_2': 'main/icons_editor/heading_2.svg',
    'heading_3': 'main/icons_editor/heading_3.svg',
    'text_bold': 'main/icons_editor/text_bold.svg',
    'text_italic': 'main/icons_editor/text_italic.svg',
    'text_line-through': 'main/icons_editor/text_line-through.svg',
    'text_underline': 'main/icons_editor/text_underline.svg',
};
var ul = document.createElement('ul');
ul.style.display = 'flex';
ul.style.flexWrap = 'wrap'
ul.style.margin = '-5px';
for (key in elements){
    var img = document.createElement('img');
    img.style.display = 'block';
    img.style.width = '100%';
    img.style.height = '100%';
    img.src = '/static/admin/js/' + elements[key];
    var li = document.createElement('li');
    li.style.cursor = 'pointer';
    li.style.flexBasis = '3%';
    li.style.margin = '5px';
    li.appendChild(img);
    ul.appendChild(li);
}
dock.appendChild(ul);
for (i=0; i<text_element.length; i++) {
   text_element[i].parentElement.appendChild(dock);
}
