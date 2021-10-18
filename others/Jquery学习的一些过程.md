**Jquery学习的一些过程**

----

* 关于表单排序

```javascript
## 第一步获取th长度
   const th_length = $('tbody > th').length
## 第二步获取当前点击th的索引值
   const this_th_index = $(this).parent('th').index()
## 第三步获取共多少行
   const tr_length = $('tbody > tr').length
## 那么就在所有td索引中找到当前th下的td， 该th下的td的索引值应该是n*th长度+th当前索引值
   const indexes = []
   for(let i =0; i< tr_length; i++){
         indexes.appends = this_th_index + i*tr_length
   }
   const indexes_values = []
## 即第一行的th下索引是当前th索引，第二行是1*th长度+当前th索引...,第N行是(n-1)*th长度+当前th索引值
9_

```

 