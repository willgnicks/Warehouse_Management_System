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
            // 如果当前元素不是多项，而是单项
            let path = "input[name='" + element + "'],select[name='" + element + "']"
            let val = $(path).val()
            if (val == "") {
                // input中为空，验证不通过，提示错误信息
                $(path).next('span').text(error_message[element]['required'])
                if (flag) {
                    flag = false
                }
            } else if (val == '请选择' || val == '请先选择入库来源') {
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