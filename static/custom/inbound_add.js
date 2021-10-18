fields = [
    'purchase',
    'pp_rel_id',
    'material_code',
    'equipment_ID',
    'comments',
]
exclude = ['comments']
error_message = {
    'purchase': {
        'invalid': '请选择正确来源'
    },
    'pp_rel_id': {
        'invalid': '请选择正确入库产品'
    },
    'material_code': {'required': '请填入物料编号'},
    'equipment_ID': {
        'required': '请填入设备ID',
        'invalid': '请输入正确的设备ID'
    },
}
cleaned_data = {}


$(function ($) {

    // 对入库来源进行判断
    $("select[name='purchase']").on('change', function () {
        let val = $(this).val()
        $('div[name="SN"]').each(function (index) {
            if (index == 0) {
                $(this).find('input').removeAttr('placeholder')
            } else {
                $(this).remove()
            }
        })

        function clean_options(after_text) {
            $("select[name='pp_rel_id']").children('option').each(function () {
                if ($(this).index() != 0) {
                    $(this).remove()
                } else {
                    $(this).text(after_text)
                }
            })
        }

        // 如果入库来源有有效数据
        if ($(this).val() != "请选择") {
            clean_options('请选择')
            // ajax请求当前采购ID下的所有未入库的pp_rel的数据
            $.ajax({
                url: '/inbounds/get_rel/',
                type: 'get',
                dataType: 'json',
                data: {'purchase_id': val},
                success: function (data) {
                    let list = data.data
                    // 将数据插入pp_rel的select中
                    for (let index in list) {
                        let obj = list[index]
                        const opt = '<option value="' + obj.id + '" name="' + obj.quantity + '">产品名称：' + obj.product__product_name
                            + '  产品型号：' + obj.product__product_model + '  数量：' + obj.quantity + '</option>'
                        $("select[name='pp_rel_id']").append(opt)
                    }
                }
            })
        } else {
            // 没有选择有效入库来源，那么入库产品没有任何选项，提示先选择入库来源
            clean_options('请先选择入库来源')
        }
    })

    $('select[name="pp_rel_id"]').on('change', function () {
        // 显示相同的设备ID的input框
        let quantity = $(this).children('option:selected').attr('name')
        $('div[name="SN"]').each(function (index) {
            if(index !== 0){
                $(this).remove()
            }else{
                $(this).find('input').attr('placeholder', '')
            }
        })
        if (quantity > 1 && quantity != undefined) {
            for (let i = 1; i < quantity; i++) {
                $('div[name="SN"]:last').after($('div[name="SN"]:first').clone(true))
            }
            $('div[name="SN"]').each(function (index) {
                let val = '请填入第' + (index + 1) + '台设备的ID'
                $(this).find('input').attr('placeholder', val)
            })
        } else {
            $('div[name="SN"]').each(function (index) {
                if (index == 0) {
                    $(this).find('input').removeAttr('placeholder')
                } else {
                    $(this).remove()
                }
            })
        }

    })


    $("#go_add").click(function () {
        if ($('#inbound_id').text() != '') {
            cleaned_data['id'] = $('#inbound_id').text()
        }
        if (valid_form(excludes_fields(fields, exclude), ['equipment_ID'])) {
            let val = $("[name='csrfmiddlewaretoken']").val()
            let comments = $("textarea[name='comments']").val()
            if (comments != null || comments != '') {
                cleaned_data['comments'] = comments
            }
            $.ajax({
                url: '/inbounds/POST/',
                type: 'POST',
                dataType: 'json',
                data: {'package_data': JSON.stringify(cleaned_data), 'csrfmiddlewaretoken': val},
                success: function (data) {
                    window.location.href = '/inbounds/'
                }
            })
        }
    });

    $("input[name='material_code'], input[name='equipment_ID']").blur(function () {
        let current = $(this)
        let query = $(this).attr('name')
        let val = $(this).val()
        if (query === 'equipment_ID') {
            query = 'equipment__SN'
        }
        $.ajax({
            url: "/inbounds/GET/" + query + "/",
            type: 'get',
            dataType: 'json',
            data: {'val': val},
            success: function (data) {
                if (parseInt(data['status']) !== 200) {
                    current.next('span').text('该内容已被占用')
                } else {
                    current.next('span').text('')
                }
            }
        })
    })


});




