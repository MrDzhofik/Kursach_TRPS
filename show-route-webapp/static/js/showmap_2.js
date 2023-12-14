var fieldIndex = 0;  // Начальный индекс для создания уникальных имен и идентификаторов
function addField() {
    var form = document.getElementById('inputContainer');
    var container = document.getElementById('input');

    // Клонируем поле выбора
    var clonedField = container.firstElementChild.cloneNode(true);

    // Увеличиваем индекс и обновляем имена и идентификаторы
    fieldIndex++;
    clonedField.querySelector('select').name = 'dynamic_field_' + fieldIndex;
    clonedField.classList.add('dynamic_field');
    clonedField.querySelector('label').textContent = 'Промежуточная точка';

    // Удаляем сообщения об ошибке
    var error_message = document.getElementsByClassName('alert');
    if (error_message.length > 0) {
        console.log(error_message.length)
        for (var i = 0; error_message.length != 0;) {
            var element = error_message[i];
            element.remove();
        }
    }
    // Добавляем клон в контейнер
    container.insertBefore(clonedField, container.children[1]);
};

function removeField() {
    // Получение ссылки на элемент по его ID
    var inputElement = document.getElementsByClassName('dynamic_field');

    // Проверка, существует ли элемент, прежде чем его удалять
    if (inputElement.length > 0) {
        // Удаление элемента
        inputElement[0].remove();
    } else {
        var errorMessage = document.createElement('p');
        errorMessage.innerText = 'Нет промежуточных точек';
        errorMessage.classList.add('alert');
        document.body.appendChild(errorMessage);
    }
}

function applyFilter() {
    // Получение выбранного значения
    var selectedValue = $("#my-select").val();

    // Отправка запроса на сервер (может потребоваться изменение URL в зависимости от вашей конфигурации)
    $.ajax({
        url: "/path/to/your/filter/view/",
        method: "GET",
        data: { filter_value: selectedValue },
        success: function (data) {
            // Обновление блока с отфильтрованными результатами
            $("#filtered-results").html(data);
        },
        error: function (error) {
            console.log("Ошибка при фильтрации: ", error);
        }
    });
}