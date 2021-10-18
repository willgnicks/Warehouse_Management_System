/**
 *
 * @param fields
 * @param exclude
 * @returns {*}
 */
function excludes_fields(fields, exclude) {
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
    return fields
}

/**
 * 对于清除了排除选项的域进行验证，将验证每个域中字段的空值与否，格式是否正确
 * @param fields 传入域
 * @param array 传入多项选项
 * @returns {} 返回验证结果
 */
function valid_form(fields, array) {
    let flag = true
    // 在clean_data中为多项创建数组
    for (let e in array) {
        cleaned_data[array[e]] = []
    }
    for (let index in fields) {
        // 遍历域中元素
        let element = fields[index]
        if ($.inArray(element, array) == -1) {
            let path = "input[name='" + element + "'],select[name='" + element + "']"
            let val = $(path).val()
            if (val == "") {
                // input中为空，验证不通过，提示错误信息
                $(path).next('span').text(error_message[element]['required'])
                if (flag) {
                    flag = false
                }
            } else if (val == '请选择' || val == '请先选择入库来源') {
                // 如果当前元素不是多项，而是单项
                // select没有选择有效选项
                $(path).next('span').text(error_message[element]['invalid'])
                if (flag) {
                    flag = false
                }
            } else {
                // input不为空，验证通过，清除错误信息
                $(path).next('span').text('')
                cleaned_data[element] = val
            }
        } else {
            // 如果当前元素不是单项，而是多项
            let path = "input[name='" + element + "'],select[name='" + element + "']"
            $(path).each(function (i) {
                // 对所有数量的input和产品的select遍历验证
                let val = $(this).val()
                if (val == "") {
                    // 如果为空，验证不通过，提示错误信息
                    if (flag) {
                        flag = false
                    }
                    $(this).next('span').text(error_message[element]['required'])
                } else if (!/^[1-9][0-9]?$/.test(val) && !/^[A-Za-z0-9]{8,16}$/.test(val)) {
                    // 验证格式是否为数字，如未选产品或填数量不为数字，验证不通过，提示错误信息
                    $(this).next('span').text(error_message[element]['invalid'])
                    if (flag) {
                        flag = false
                    }
                } else {
                    // 验证通过，清除错误信息
                    $(this).next('span').text('')
                    cleaned_data[element][i] = val
                }
            })
        }

    }
    return flag
}


function insert_a() {
    const asc_a = '<a style="float: left; margin-top: 2px" class="fa fa-sort-amount-asc"></a>'
    const desc_a = '<a style="float: right; margin-top: 2px" class="fa fa-sort-amount-desc"></a>'
    const th = $('thead > tr > th')
    th.each(function (index) {
        const length = th.length - 1
        if (index !== 0 && index !== length) {
            $(this).append(asc_a)
            $(this).children().last().after(desc_a)

        }
    })
}

//文档加载优先级最高
$(document).ready(function () {
    insert_a()
});
// //文档加载事件二
// $(function(){
// 	// alert("文档加载完成2!");
// });

$(function ($) {

    function is_int(a) {
        return /^[0-9]*$/.test(Object.values(a)[0])
    }

    // 降序排序
    const int_asc = function (a, b) {
        return Object.values(b)[0] - Object.values(a)[0]
    }
    const str_asc = function (a, b) {
        return Object.values(b)[0].localeCompare(Object.values(a)[0]);
    }
    // 升序排序
    const int_desc = function (a, b) {
        return Object.values(a)[0] - Object.values(b)[0]
    }
    const str_desc = function (a, b) {
        return Object.values(a)[0].localeCompare(Object.values(b)[0]);

    }
    // 获取该列全部数据并返回
    const get_content = function (index, tr_length, th_length) {
        let index_content = []
        for (let i = 0; i < tr_length; i++) {
            let this_td = th_length * i + index
            let text = $('tbody > tr > td').eq(this_td).text().trim()
            let temp = {}
            temp[i] = text
            index_content[i] = temp
        }
        return index_content
    }
    //  0是desc操作， 1是asc操作
    const sort_table = function (this_td_index, operation) {

        let table = $('tbody')
        let clone = table.clone(true)
        clone.children('tbody > tr').remove()
        const all_tr = $('tbody > tr')

        // # 第一步获取th长度
        const th_length = $('thead > tr > th').length
        // # 第二步获取当前点击th的索引值
        // # 第三步获取共多少行
        const tr_length = all_tr.length
        // 取排序内容
        let content = get_content(this_td_index, tr_length, th_length)
        let value = content[0][0]
        // 排序
        if (operation === 0) {
            if (is_int(value)) {
                content.sort(int_desc)
            } else {
                content.sort(str_desc)
            }
        } else if (operation === 1) {
            if (is_int(value)) {
                content.sort(int_asc)
            } else {
                content.sort(str_asc)
            }
        }
        // 获得排序后的index序列
        let sorted_keys = []
        for (let index in content) {
            sorted_keys.push(Object.keys(content[index])[0])
        }
        // 对clone插入值
        let len = clone.children('tr').length
        for (let i = 0; i < tr_length; i++) {
            let sorted_index = parseInt(sorted_keys[i])
            let sorted_tr = table.children('tr').eq(sorted_index).clone(true)
            let text = i + 1
            sorted_tr.children('td:eq(0)').text(text)
            if (len === 0) {
                clone.append(sorted_tr)
            } else {
                clone.children('tr:last').after(sorted_tr)
            }
        }
        // 替换table
        table.replaceWith(clone)
    }
    // 升序
    $(".fa-sort-amount-asc").on('click', function () {
        const this_td_index = $(this).parent('th').index()
        sort_table(this_td_index, 0)
    })
    // 降序
    $(".fa-sort-amount-desc").click(function () {
        const this_td_index = $(this).parent('th').index()
        sort_table(this_td_index, 1)
    })


})