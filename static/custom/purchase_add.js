// 采购产品种类的计数器
counter = 1
// 字段的域，对应表单中的各个项的name
fields = [
    'form_number',
    'contract_number',
    'demand_person',
    'handle_man',
    'quantity',
    'product',
]
// 字段域的排除项
exclude = []
// 回显的错误信息
error_message = {
    'form_number': {'required': '请输入采购单号'},
    'contract_number': {'required': '请填入合同号'},
    'demand_person': {'required': '请填入需求人'},
    'handle_man': {'required': '请填入经手人'},
    'quantity': {'required': '请填入数量', 'invalid': '请填入正确数量'},
    'product': {'invalid': '请选择产品'},
}
// 选中的产品名称list
selected = []
// 校验的最终有效数据
cleaned_data = {}
// 采购单的ID
purchase_id = 0


/**
 * 加载页面去查询该数据，如果数据存在，那么修改counter
 * @returns {*|Window.django.jQuery}
 */
function load_by_page() {

    let product_len = $("#product_len").text()
    let purchase = $("#purchase_id").text()
    let product = []
    // 获取数据长度
    if (product_len !== "") {
        counter = product_len
    }
    // 获取当前采购单的ID
    if (purchase !== "") {
        purchase_id = purchase
    }
    // 循环获取所有产品选项
    $("select[name='product']").each(function (index) {
        let val = $(this).val()
        selected[index] = $(this).children("option[value='" + val + "']").text()
        product[index] = val
    })
    for (let index in product) {
        remove_or_append(index, product[index], 0)
    }
}

/**
 *   将除过当前select的所有select中的当前option的值全部删除或增加
 * @param selected_index 监听选择框在所有该类选择框的索引
 * @param selected_option_value remove传当前val，append传改变前previous
 * @param operation remove操作为0，append操作为1，传其他参数提示错误
 */
function remove_or_append(selected_index, selected_option_value, operation) {
    $("select[name='product']").each(function (index) {
        if (parseInt(selected_index) !== index) {
            if (operation === 0) {
                $("select[name='product']").eq(index).children("option[value='" + selected_option_value + "']").remove()
            } else if (operation === 1) {
                let option = "<option value='" + selected_option_value + "'>" + selected[selected_index] + "</option>"
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
    }
    // previous是product选择变化前的值
    let previous
    $("select[name='product']").on('click focus', function () {
        // 当选择框被单击或获得焦点，获取此时的选择框的值，此时值为更改前的值，用click和focus为兼容safari和chrome
        // 如果当前的值是请选择，那么previous的值设为-1；
        // 如不是，那就能获得对应产品id，那么previous的值修改为对应id
        let val = $(this).val()
        if (val !== "请选择") {
            previous = val
        } else {
            previous = -1
        }
    }).change(function () {
        // 当选择框内值发生改变，那么获取改变后的值，并且获取该选择框在所有该类选择框的索引
        let this_index = $(this).index("select[name='product']")
        let val = $(this).val()
        if (val !== '请选择') {
            let text = $(this).children("option[value='" + val + "']").text()
            if (previous === -1) {
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
        if (val !== '请选择') {
            $("div[name='product_unit']:last").find($("option[value='" + val + "']")).remove()
        }

        counter += 1
    });

    $('#minus').click(function () {
        // counter等于1，那么只剩一行产品，此时不能再删除产品行
        if (counter > 1) {
            let val = $("select[name='product']:last").val()
            if (val !== '请选择') {
                // 删除该行时，如果该行有选的值，该值必然在selected中，那么需要删除该行前将已选项释放显示，从数组中删除，删除完成后再删除改行
                let this_index = $("select[name='product']:last").index("select[name='product']")
                remove_or_append(this_index, val, 1)
                selected.splice(this_index, 1)

            }
            // 如果删除该行时，该行没有选值，直接删除改行
            $("div[name='product_unit']:last").remove()
            counter -= 1
        }


    });

    $("#go_add").click(function () {
        if (purchase_id !== 0) {
            cleaned_data['id'] = purchase_id
        }
        if (valid_form(excludes_fields(fields, exclude), ['product', 'quantity'])) {
            let project_val = $("select[name='project']").val()
            if (project_val !== '请选择') {
                cleaned_data['project_id'] = project_val
            }
            let val = $("[name='csrfmiddlewaretoken']").val()
            $.ajax({
                url: '/purchases/POST/',
                type: 'POST',
                dataType: 'json',
                data: {'package_data': JSON.stringify(cleaned_data), 'csrfmiddlewaretoken': val},
                success: function (data) {
                    if (parseInt(data.status) === 200) {
                        window.location.href = '/purchases/'
                    }
                }
            })
        }
    });

    $("input[name='form_number'], input[name='contract_number']").blur(function () {
        let query = $(this).attr('name')
        let val = $(this).val()
        $.ajax({
            url: "/purchases/GET/" + query + "/",
            type: 'get',
            dataType: 'json',
            data: {'val': val},
            success: function (data) {
                if (data['status'] === 'unavailable') {
                    $("input[name='" + data['component'] + "']").next('span').text('该编号已被使用')
                } else {
                    $("input[name='" + data['component'] + "']").next('span').text('')
                }
            }
        })
    })


});




