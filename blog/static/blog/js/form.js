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
    komu: $('#next-btn'),
    skolko: $('#skolko-btn'),
    prosrochky: $('#prosrochky-btn'),
    zalogi: $('#zalogi-btn'),
    name: $('#name-btn'),
    sendFormBtn: $('#send-form-btn')
  }
};

let flow = {
  'komu': {
    step: 1,
    value: null,
  },
  "skolko": {
    step: 2,
    value: null,
  },
  "prosrochky": {
    step: 3,
    value: null,
  },
  "zalogi": {
    step: 4,
    value: null,
  },
  "name": {
    step: 5,
    value: null,
  },
  "phone": {
    step: 6,
    value: null,
  },
  "state": {
    step: null
  }

}

let view = {
  init: function () {
    
    view.render()
  },

  render: function () {
//     html.btn.komu.click(function (event) {
//       html.form.komu.fadeToggle("slow", function () {
//         html.form.skolko.fadeToggle("slow", function () {
//           html.btn.skolko.click(function () {
//             html.form.skolko.fadeToggle("slow", function () {
//               html.form.prosrochky.fadeToggle("slow", function () {
//                 html.btn.prosrochky.click(function () {
//                   html.form.prosrochky.fadeToggle("slow", function () {
//                     html.form.zalogi.fadeToggle("slow", function () {
//                       html.btn.zalogi.click(function () {
//                         html.form.zalogi.fadeToggle("slow", function () {
//                           html.form.name.fadeToggle("slow", function () {
//                             html.btn.name.click(function () {
//                               html.form.name.fadeToggle("slow", function () {
//                                 html.form.phone.fadeToggle("slow")
//                               })

//                             })
//                           })
//                         })

//                       })
//                     })
//                   })
//                 })
//               })
//             })
//           })
//         })
//       })
//     })
//   }
  return
 }
}
let controller = {
  init: function () {
    return view.init()
  },
};

controller.init()

/**
 * 
 * Отобразить форму "Кому вы долны ?"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 * 
 */

 // TODO: Пройти по объекту html в цикле и записать все дальнейшее дейсто в 2-3 функциях
$(function () {
   
  html.form.komu.find('input').on('change', function () {
    
    if ($(this).prop('checked')) {
      
      html.btn.komu.attr('disabled', false)
      
    } else {

      html.btn.komu.attr('disabled', true)
    }
  })
})

/**
 * 
 * Отобразить форму "Сколько вы должны ?"
 * отслеживть изменения ввода
 * если выбран ответ
 * Кнопка "Дальше" не отключенна
 * иначе кнопка выключена
 * 
 */
$(function () {
  let input = html.form.skolko.find('input').on('change', function (
  ) {
    if ($(this).prop('checked')) {
      html.btn.skolko.attr('disabled', false)
    } else {
      html.btn.skolko.attr('disabled', true)
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
    } else {
      html.btn.prosrochky.attr('disabled', true)
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
    } else {
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