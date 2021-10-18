// 出库产品的计数器
counter = 1
// 字段的域，对应表单中的各个项的name
fields = [
    'project_id',
    'demand_person',
    'contract_number',
    'form_number',
    'outbound_date',
    'flag',
    'equipment',
]
// 字段域的排除项
exclude = ['flag','outbound_date',]
// 回显的错误信息
error_message = {
    'project_id': {'invalid': '请选择出库的项目'},
    'demand_person': {'required': '请填写申请人姓名'},
    'contract_number': {'required': '请填写销售合同编号'},
    'form_number': {'required': '请填写出库表单号'},
    'equipment': {'invalid': '请选择出库的设备'},
}
// 选中的产品名称list
selected = []
// 校验的最终有效数据
cleaned_data = {}
// 采购单的ID
outbound_id = 0


/**
 * 加载页面去查询该数据，如果数据存在，那么修改counter
 * @returns {*|Window.django.jQuery}
 */
// function load_by_page() {
//
//     let product_len = $("#product_len").text()
//     let purchase = $("#purchase_id").text()
//     let product = []
//     // 获取数据长度
//     if (product_len !== "") {
//         counter = product_len
//     }
//     // 获取当前采购单的ID
//     if (purchase !== "") {
//         purchase_id = purchase
//     }
//     // 循环获取所有产品选项
//     $("select[name='product']").each(function (index) {
//         let val = $(this).val()
//         selected[index] = $(this).children("option[value='" + val + "']").text()
//         product[index] = val
//     })
//     for (let index in product) {
//         remove_or_append(index, product[index], 0)
//     }
// }

/**
 *   将除过当前select的所有select中的当前option的值全部删除或增加
 * @param selected_index 监听选择框在所有该类选择框的索引
 * @param selected_option_value remove传当前val，append传改变前previous
 * @param operation remove操作为0，append操作为1，传其他参数提示错误
 */
function remove_or_append(selected_index, selected_option_value, operation) {
    $("select[name='equipment']").each(function (index) {
        if (parseInt(selected_index) !== index) {
            if (operation === 0) {
                $("select[name='equipment']").eq(index).children("option[value='" + selected_option_value + "']").remove()
            } else if (operation === 1) {
                let option = "<option value='" + selected_option_value + "'>" + selected[selected_index] + "</option>"
                $("select[name='equipment']").eq(index).append(option)
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
    let previous
    $("select[name='equipment']").on('click focus', function () {
        let val = $(this).val()
        if (val !== "请选择") {
            previous = val
        } else {
            previous = -1
        }
    }).change(function () {
        let this_index = $(this).index("select[name='equipment']")
        let val = $(this).val()
        if (val !== '请选择') {
            let text = $(this).children("option[value='" + val + "']").text()
            if (previous === -1) {
                selected[this_index] = text
                remove_or_append(this_index, val, 0)
            } else {
                remove_or_append(this_index, previous, 1)
                selected[this_index] = text
                remove_or_append(this_index, val, 0)
            }
        } else {
            if (previous > 0) {
                remove_or_append(this_index, previous, 1)
            }
        }
    });
    /**
     * 增加产品行按钮的点击事件，从最后的一个组件后增加一个该组件
     */
    $("#plus").click(function () {
        // 第一步先将第一个div block克隆
        let block = $("div[name='outbound_unit']:first").clone(true)
        // 第二步如果克隆的block中有选中的有效值，将其option删除
        let val = $("select[name='equipment']:first").val()
        console.log(val)
        if (val !== '请选择') {
            console.log(block)
            let option = "option[value='" + val + "']"
            console.log(option)
            block.find(option).remove()
            console.log(block)
        }
        // 第三步将block插入最后的位置
        $("div[name='outbound_unit']:last").after(block)
        counter += 1
    });

    $('#minus').click(function () {
        // counter等于1，那么只剩一行产品，此时不能再删除产品行
        if (counter > 1) {
            let last_select = $("select[name='equipment']:last")
            let val = last_select.val()
            if (val !== '请选择') {
                let this_index = last_select.index("select[name='equipment']")
                remove_or_append(this_index, val, 1)
                selected.splice(this_index, 1)

            }
            // 如果删除该行时，该行没有选值，直接删除改行
            $("div[name='outbound_unit']:last").remove()
            counter -= 1
        }


    });

    $("#go_add").click(function () {
        if (valid_form(excludes_fields(fields, exclude), ['equipment'])) {
            console.log(cleaned_data)
            let val = $("[name='csrfmiddlewaretoken']").val()
            $.ajax({
                url: '/outbounds/POST/',
                type: 'POST',
                dataType: 'json',
                data: {'package_data': JSON.stringify(cleaned_data), 'csrfmiddlewaretoken': val},
                success: function (data) {
                    if (parseInt(data.status) === 200) {
                        window.location.href = '/outbounds/'
                    }
                }
            })
        }
    });
    //
    // $("input[name='form_number'], input[name='contract_number']").blur(function () {
    //     let query = $(this).attr('name')
    //     let val = $(this).val()
    //     $.ajax({
    //         url: "/purchases/GET/" + query + "/",
    //         type: 'get',
    //         dataType: 'json',
    //         data: {'val': val},
    //         success: function (data) {
    //             if (data['status'] === 'unavailable') {
    //                 $("input[name='" + data['component'] + "']").next('span').text('该编号已被使用')
    //             } else {
    //                 $("input[name='" + data['component'] + "']").next('span').text('')
    //             }
    //         }
    //     })
    // })


});




