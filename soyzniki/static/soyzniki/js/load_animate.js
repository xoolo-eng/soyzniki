function start_animate(){
    var animate_block =  {
        load_animate: document.createElement('div'),
        content_animate: document.createElement('div'),
        circle1: document.createElement('div'),
        circle2: document.createElement('div')
    };
    animate_block.load_animate.id = 'load_animate';
    animate_block.content_animate.id = 'content_animate';
    animate_block.circle1.id = 'circle1';
    animate_block.circle2.id = 'circle2';
    animate_block.content_animate.appendChild(animate_block.circle1);
    animate_block.content_animate.appendChild(animate_block.circle2);
    animate_block.load_animate.appendChild(animate_block.content_animate);
    var body = document.getElementsByTagName('body')[0];
    body.appendChild(animate_block.load_animate);
}

function stop_animate(){
    var load_animate = document.getElementById('load_animate');
    load_animate.remove();
}