counter = 1
path = 'product'
fields = [
    'form_number',
    'contract_number',
    'demand_person',
    'handle_man',
    'quantity',
    'product',
]
type = ['char', 'char', 'char', 'char', 'number', 'select']
exclude = []
error_message = {
    'form_number': {'required': '请输入采购单号'},
    'contract_number': {'required': '请填入合同号'},
    'demand_person': {'required': '请填入需求人'},
    'handle_man': {'required': '请填入经手人'},
    'quantity': {'required': '请填入数量', 'invalid': '请填入正确数量'},
    'product': {'invalid': '请选择产品'},
}
selected = []
cleaned_data = {}
product = []
quantity = []
purchase_id = 0

// onchange:valid_form(fields, exclude)

function excludes_fields(){
    // 排除选项数组中有内容
    if (exclude.length > 0) {
        // 遍历排除选项，如域中有排除选项中的元素，将其删除
        for (let element of exclude) {
            let index = fields.indexOf(element)
            if (index >= 0) {
                fields.splice(index, 1)
            }
        }
    }
}
/**
 * 对于清除了排除选项的域进行验证，将验证每个域中字段的空值与否，格式是否正确
 * @param fields 传入域
 * @param exclude 传入排除选项
 * @returns {boolean} 返回验证结果
 */
function valid_form() {
    let flag = true
    for (let index in fields) {
        let element = fields[index]
        if (element != 'product' && element != 'quantity') {
            // 遍历域中元素，如果该元素不为产品或数量时
            let path = "input[name='" + element + "']"
            let val = $(path).val()
            if (val == "") {
                // input中为空，验证不通过，提示错误信息
                $(path).next('span').text(error_message[element]['required'])
                if (flag) {
                    flag = false
                }
            } else {

                // input不为空，验证通过，清除错误信息
                $(path).next('span').text('')
                cleaned_data[element] = val
            }
        } else {
            // 如果是产品或者数量时，那么选择器双重条件选取产品和数量
            let path = "input[name='" + element + "'],select[name='" + element + "']"
            $(path).each(function (index) {
                // 对所有数量的input和产品的select遍历验证
                let val = $(this).val()
                if (val == "") {
                    // 如果为空，验证不通过，提示错误信息
                    if (flag) {
                        flag = false
                    }
                    $(this).next('span').text(error_message[element]['required'])
                } else if (!/^[1-9]\d*$/.test(val)) {
                    // 验证格式是否为数字，如未选产品或填数量不为数字，验证不通过，提示错误信息
                    $(this).next('span').text(error_message[element]['invalid'])
                    if (flag) {
                        flag = false
                    }
                } else {
                    // 验证通过，清除错误信息
                    $(this).next('span').text('')
                    if (element == 'product') {
                        product[index] = val
                    } else {
                        quantity[index] = val
                    }
                }
            })
        }

    }
    return flag
}

/**
 * 加载页面去查询该数据，如果数据存在，那么修改counter
 * @returns {*|Window.django.jQuery}
 */
function load_by_page() {

    let product_len = $("#product_len").text()
    let purchase = $("#purchase_id").text()
    if (product_len != "") {
        counter = product_len
    }
    if (purchase != "") {
        purchase_id = purchase
    }
    $("select[name='product']").each(function (index) {
        let val = $(this).val()
        let text = $(this).children("option[value='" + val + "']").text()
        selected[index] = text
        product[index] = val
    })
    $("input[name='quantity']").each(function (index) {
        quantity[index] = $(this).val()
    })
    for (let index in product) {
        remove_or_append(index, product[index], 0)

    }
}
// function is_this_occupied(keyword,value){
//     let path = '/purchases/'+keyword+'/'
//     $.ajax({
//         url: path,
//         dataType: 'json',
//         type: 'get',
//         data: {'request': value},
//         success:function (data){
//             return data
//         }
//     })
//
//
//
//
// }

/**
 *
 * @param selected_index 监听选择框在所有该类选择框的索引
 * @param selected_option_value remove传当前val，append传改变前previous
 * @param operation remove操作为0，append操作为1，传其他参数提示错误
 */
function remove_or_append(selected_index, selected_option_value, operation) {
    $("select[name='product']").each(function (index) {
        if (selected_index != index) {
            if (operation == 0) {
                $("select[name='product']").eq(index).children("option[value='" + selected_option_value + "']").remove()
            } else if (operation == 1) {
                let option = "<option value='" + selected_option_value + "'>" + selected[selected_index] + "</option>"
                console.log(option)
                $("select[name='product']").eq(index).append(option)
            } else {
                alert("传入操作有误，0为remove，1为append")
            }

        }
    })
}

$(function ($) {
    window.onload = function () {
        load_by_page()
        excludes_fields()
    }

    let previous
    $("select[name='product']").on('click focus', function () {
        // 当选择框被单击或获得焦点，获取此时的选择框的值，此时值为更改前的值，用click和focus为兼容safari和chrome
        // 如果当前的值是请选择，那么previous的值设为-1；
        // 如不是，那就能获得对应产品id，那么previous的值修改为对应id
        let val = $(this).val()
        if (val != "请选择") {
            previous = val
        } else {
            previous = -1
        }
    }).change(function () {
        // 当选择框内值发生改变，那么获取改变后的值，并且获取该选择框在所有该类选择框的索引
        let this_index = $(this).index("select[name='product']")
        let val = $(this).val()
        if (val != '请选择') {
            let text = $(this).children("option[value='" + val + "']").text()
            if (previous == -1) {
                // 改变前的值为请选择，改变后的值不为请选择,将该值插入数组，并隐藏该值对应选项
                console.log(selected)
                selected[this_index] = text
                console.log(selected)
                remove_or_append(this_index, val, 0)
            } else {
                // 改变前的值不为请选择，改变后的值不为请选择
                // 那么显示改变前值对应选项并从数组删除，那么隐藏改变后值对应选项并将该值插入数组

                remove_or_append(this_index, previous, 1)
                console.log(selected)
                selected[this_index] = text
                console.log(selected)
                remove_or_append(this_index, val, 0)
            }
        } else {
            // 改变后的值为请选择，将改变前值对应选项显示并从数组中删除
            if (previous > 0) {
                remove_or_append(this_index, previous, 1)
            }
        }
    });
    /**
     * 增加产品行按钮的点击事件，从最后的一个组件后增加一个该组件
     */
    $("#plus").click(function () {
        let block = $("div[name='product_unit']:first").clone(true)
        let input_val = block.find('input').val()
        if (input_val != null) {
            block.children('div').children('input').val("")
        }
        $("div[name='product_unit']:last").after(block)
        let val = $("select[name='product']:first").val()
        if (val != '请选择') {
            $("div[name='product_unit']:last").find($("option[value='" + val + "']")).remove()
        }

        counter += 1
    });

    $('#minus').click(function () {
        // counter等于1，那么只剩一行产品，此时不能再删除产品行
        if (counter > 1) {
            let val = $("select[name='product']:last").val()
            let q = $("input[name='quantity']:last").val()
            if (val != '请选择') {
                // 删除该行时，如果该行有选的值，该值必然在selected中，那么需要删除该行前将已选项释放显示，从数组中删除，删除完成后再删除改行
                product.splice(product.indexOf(val), 1)
                quantity.splice(quantity.indexOf(q), 1)
                let this_index = $("select[name='product']:last").index("select[name='product']")
                remove_or_append(this_index, val, 1)
                selected.splice(this_index,1)

            }
            // 如果删除该行时，该行没有选值，直接删除改行
            $("div[name='product_unit']:last").remove()
            counter -= 1
        }


    });

    $("#go_add").click(function () {
        if (valid_form()) {
            console.log(cleaned_data)
            let project_val = $("select[name='project']").val()
            if (project_val != '请选择') {
                cleaned_data['project_id'] = project_val
            }
            cleaned_data['product'] = product
            cleaned_data['quantity'] = quantity
            let val = $("[name='csrfmiddlewaretoken']").val()

            $.ajax({
                url: '/purchases/purchase/',
                type: 'POST',
                dataType: 'json',
                data: {'package_data': JSON.stringify(cleaned_data), 'csrfmiddlewaretoken': val},
                success: function (data) {
                    window.location.href = '/purchases/'
                }

            })

        }


    });


});




