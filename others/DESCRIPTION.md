**出库模块**

---

1. 出库设备只能当设备可用，也就是设备的状态的在库

   ```python
   # 解决方式 显示equipment的时候，status_code=0
   fields = ['条件']
   Equipment.objects.filter(flag=1, status_code=0).values(*fields)
   ```

   

2. 出库模块外键项目模型ID，在甄选所有出库设备时可以正向查询设备都出库给哪个项目了

   ```python
   # 解决方式 
   Outbound.objects.filter('条件').values(*['project_name'])
   ```

   

3. 出库模型跟设备模型是一对多的关系，一个出库可以出多台设备

   ```python
   # 解决方式
   Outbound.objects.filter('condition').values(*['equipment'])
   ```

   

**Django中的一些坑**

----

* 模型的排序

  ```python
  ## 通过model.objects.last()取最后一个model，那么就必须要注意在model.py中的class Meta中的ordering
  ## 这是一个类，通过flag排序
  class Test(models.Model):
      class Meta:
          ordering=['flag']
  ## 取该类数据库中最后一个Test对象
  test = Test.objects.last()
  ## 此时test的根据flag排序的最后一个，如果取最后一Test的ID
  this_id = test.id  ## 这是flag排序最后一个Test对象的id，不是id最大的一个
  ## 那么取id最大的有怎么办
  ## 第一种是改Test中的ordering=['id']，那么此时取最大id
  max_id = Test.objects.last().id
  ## 第二种是不更改odering，那么此时取最大id
  max_id = Test.objects.all().order_by('id').last().id
          
  ```

  

