let html = {
  form: {
    komu: $('#komu'),
    skolko: $('#skolko'),
    prosrochky: $('#prosrochky'),
    zalogi: $('#zalogi'),
    name: $('#name'),
    phone: $('#phone')
  },
  btn: {
    komu: $('#next-komu-btn'),
    skolko: $('#next-skolko-btn'),
    prosrochky: $('#next-prosrochky-btn'),
    zalogi: $('#next-zalogi-btn'),
    name: $('#next-name-btn'),
    sendFormBtn: $('#send-form-btn')
  }
};

let view = {
  init: function () {
    view.render()
  },

  render: function () {

    return
 }
}

let controller = {
  init: function () {
    return view.init()
  },
};

controller.init()

$(function() {
  'use strict';
  
  window.addEventListener('load', function() {
    
    var forms = document.getElementsByClassName('needs-validation');
    
    var validation = Array.prototype.filter.call(forms, function(form){
      form.addEventListener('submit', function(event){
        if (form.checkValidity() == false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
});

/**
 * Отобразить форму "Сколько вы должны ?"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 */
$(function () {
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
    delay: { "show": 700, "hide": 100 }
  })
})

$(function () {
   
  html.form.skolko.find('input').on('change', function () {
    
    if ($(this).prop('checked')) {
      html.btn.skolko.attr('disabled', false);
      html.btn.skolko.css("pointer-events", "unset");
      $("#skolko-next-popover").popover('dispose');
      
    } else {
      html.btn.skolko.css("pointer-events", "none");
      html.btn.skolko.attr('disabled', true);
      $("#skolko-next-popover").popover();
    }
  })
})


/**
 * Отобразить форму "Кому вы долны ?"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 */
 // TODO: Пройти по объекту html в цикле и записать все дальнейшее дейсто в 2-3 функциях
 $(function () {
   
  html.form.komu.find('input').on('change', function () {
    
    if ($(this).prop('checked')) {
      html.btn.komu.attr('disabled', false)
      html.btn.komu.css("pointer-events", "unset");
      $("#komu-next-popover").popover('dispose');
    } else {
      html.btn.komu.css("pointer-events", "none");
      $("#komu-next-popover").popover({trigger: "hover", container: 'body'});
      html.btn.komu.attr('disabled', true)
    }
  })
})
/**
 * 
 * Отобразить форму "Просрочки ?"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 * 
 */
$(function () {
  html.form.prosrochky.find('input').on('change', function () {
    if ($(this).prop('checked')) {
      html.btn.prosrochky.attr('disabled', false)
      html.btn.prosrochky.css("pointer-events", "unset");
      $("#prosrochky-next-popover").popover('dispose');
    } else {
      html.btn.prosrochky.css("pointer-events", "none");
      html.btn.prosrochky.attr('disabled', true);
      $("#prosrochky-next-popover").popover('enable');
    }
  })
})

/**
 * 
 * Отобразить форму "Залоги ?"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 * 
 */
$(function () {
  html.form.zalogi.find('input').on('change', function () {
    if ($(this).prop('checked')) {
      html.btn.zalogi.attr('disabled', false)
      html.btn.zalogi.css("pointer-events", "unset");
      $("#zalogi-next-popover").popover('dispose');
    } else {
      html.btn.zalogi.css("pointer-events", "none");
      $("#zalogi-next-popover").popover('enable');
      html.btn.zalogi.attr('disabled', true)
    }
  })
})

/**
 * 
 * Отобразить форму "Имя"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 * 
 */
$(function(){
  html.form.name.find('input').on('change', function(event){
    event.preventDefault();
    if (event) {
      html.btn.name.attr('disabled', false)
      html.btn.name.css("pointer-events", "unset");
      $("#name-next-popover").popover('dispose');
    } else {
      html.btn.name.css("pointer-events", "none");
      $("#name-next-popover").popover('enable');
      html.btn.name.attr('disabled', true)
    }
  })
})

/**
 * 
 * Отобразить форму "Имя"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 * 
 */
$(function(){
  html.form.phone.find('input').on('change', function(event){
    event.preventDefault();
    if (event) {
      html.btn.sendFormBtn.attr('disabled', false)
    } else {
      html.btn.sendFormBtn.attr('disabled', true)
    }
  })
})
/**
 * 
 * Отслеживать нажатия выключенной кнопки дальше
 * Если она нажата, скрыть форму
 * Показать сообщение об ошибке пользователю
 * Отслеживать нажатие кнопки закрыть сообщение
 * если она нажата скрыть сообщение об ошибке
 * показать форму
 * 
 * */

  $("#next-btn").mousedown((function () {
    if ($(this).attr('disabled') === 'disabled') {
      html.form.komu.fadeToggle(function () {
        $("#alert").fadeToggle()
      })
    }
  }))

$("#errorMessage").click((function () {
  $("#next-btn").mousedown()
}))

$('#alert-close-btn').click(function () {
  $('#alert').fadeToggle(function () {
    html.form.komu.fadeToggle()
  })
});

