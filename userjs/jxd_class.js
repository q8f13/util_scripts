// Jing Xun Ding auto hangup js script
// auto anti-afk, auto next chapter, even auto face-detection if you can hang a portrait or use fake-camera input
// copy paste this script into console in browser web developer tools for usage

function check_btn(){
    // var t = $('.next_button___YGZWZ')
    var t = document.getElementsByClassName("next_button___YGZWZ")[0]
    if(t){
        t.click()
      console.log('next')
      return
    }
  
  var ss = document.getElementsByClassName("prism-big-play-btn")[0]
  // var ss = $('.prism-big-play-btn')
  if(!isHidden(ss)){
    ss.click()
    console.log('start')
    return
  }

  var ant = document.getElementsByClassName('ant-btn-primary')[0]
  // var ant = $('.ant-btn-primary')
  if(ant && !isHidden(ant)){
    ant.click()
    console.log('ant ant btn')
    return
  }
  
  console.log('nothing')
}

function isHidden(el) {
    var style = window.getComputedStyle(el);
    return (style.display === 'none')
}

setInterval(check_btn, 10000)

