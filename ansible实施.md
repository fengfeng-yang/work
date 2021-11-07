#### 一、要解决的问题

- 需要一起执行的脚本文件放在哪里？
- 主机如何分组管理？
- 不同的管理员如何使用ansible
- ansible如何实现自动化

#### 二、ansible介绍

1. 什么是ansible？

   Ansible 简单的说是一个配置管理系统(configuration management system)。你只需要可以使用 ssh 访问你的服务器或设备就行。

2. ansible可以帮助我们做什么？

   ansible可以帮助我们完成一些批量任务，或者完成一些需要经常重复的工作。比如：同时在100台服务器上安装nginx服务，并在安装后启动它们。比如：将某个文件一次性拷贝到100台服务器上。比如：每当有新服务器加入工作环境时，你都要为新服务器部署某个服务，也就是说你需要经常重复的完成相同的工作。这些场景中我们都可以使用到ansible。。

   包括：拷贝文件、安装包、启动服务等等

   

#### 三、ansible的架构	

1. ##### ansible 包括了主机清单（Inventory）、模块、

2. ##### 什么是 Host Inventory

   Host Inventory 是配置文件，用来告诉Ansible需要管理哪些主机。并且把这些主机根据按需分类。

   **可以根据用途分类**：数据库节点，服务节点等；根据地点分类：中部，西部机房。

   Host Inventory 默认的文件是： **/etc/ansible/hosts**

3. ##### Ansible用命令管理主机

   Ansible提供了一个命令行工具，在官方文档中起给命令行起了一个名字叫Ad-Hoc Commands。

   ansible命令的格式是：

   ```
   ansible <host-pattern> [options]
   #启动服务
   ansible web -m service -a "name=httpd state=started"
   #查看远程主机的全部系统信息！！！
   ansible all -m setup
   ```

4. ##### ansible模块

   bash无论在命令行上执行，还是bash脚本中，都需要调用cd、ls、copy、yum等命令；module就是Ansible的“命令”，module是ansible命令行和脚本中都需要调用的。常用的Ansible module有yum、copy、template等。

   在bash，调用命令时可以跟不同的参数，每个命令的参数都是该命令自定义的；同样，ansible中调用module也可以跟不同的参数，每个module的参数也都是由module自定义的。

   ###### Ansible在命令行里使用Module

   在命令行中

   > -m后面接调用module的名字
   >
   > -a后面接调用module的参数

   ```
   #使用module copy拷贝管理员节点文件/etc/hosts到所有远程主机/tmp/hosts
   ansible all -m copy -a "src=/etc/hosts dest=/tmp/hosts"
   #使用module yum在远程主机web上安装httpd包
   ansible web -m yum -a "name=httpd state=present"
   ```

   ###### Ansible在Playbook脚本使用Module

   在playbook脚本中，tasks中的每一个action都是对module的一次调用。在每个action中：

   > 冒号前面是module的名字
   >
   > 冒号后面是调用module的参数

   ```
   ---
     tasks:
     - name: ensure apache is at the latest version
       yum: pkg=httpd state=latest
     - name: write the apache config file
       template: src=templates/httpd.conf.j2 dest=/etc/httpd/conf/httpd.conf
     - name: ensure apache is running
       service: name=httpd state=started
   ```

5. ##### ansible剧本

   ###### Ansible用脚本管理主机

   只有脚本才可以重用，避免总敲重复的代码。Ansible脚本的名字叫Playbook，使用的是YAML的格式，文件以yml结尾。

   注解：YAML和JSON类似，是一种表示数据的格式。

   ###### 执行脚本playbook的方法

   ```
   ansible-palybook deploy.yml
   ```

   ###### playbook的例子

   deploy.yml的功能为web主机部署apache, 其中包含以下部署步骤：

   1. 安装apache包；
   2. 拷贝配置文件httpd，并保证拷贝文件后，apache服务会被重启；
   3. 拷贝默认的网页文件index.html；
   4. 启动apache服务；

   playbook deploy.yml包含下面几个关键字，每个关键字的含义：

   - **hosts**：为主机的IP，或者主机组名，或者关键字all

   - **remote_user**: 以哪个用户身份执行。

   - **vars**： 变量

   - **tasks**: playbook的核心，定义顺序执行的动作action。每个action调用一个ansbile module。

   - > action 语法： `module： module_parameter=module_value`

   - > 常用的module有yum、copy、template等，module在ansible的作用，相当于bash脚本中yum，copy这样的命令。下一节会介绍。

   - **handers**： 是playbook的event，默认不会执行，在action里触发才会执行。多次触发只执行一次。

   ```
   ---
   - hosts: web
     vars:
       http_port: 80
       max_clients: 200
     remote_user: root
     tasks:
     - name: ensure apache is at the latest version
       yum: pkg=httpd state=latest
   
     - name: Write the configuration file
       template: src=templates/httpd.conf.j2 dest=/etc/httpd/conf/httpd.conf
       notify:
       - restart apache
   
     - name: Write the default index.html file
       template: src=templates/index.html.j2 dest=/var/www/html/index.html
   
     - name: ensure apache is running
       service: name=httpd state=started
     handlers:
       - name: restart apache
         service: name=httpd state=restarted
   ```

6. ##### ansible角色（roles）

   Roles 基于一个已知的文件结构，去自动的加载某些 vars_files，tasks 以及 handlers。基于 roles 对内容进行分组，使得我们可以容易地与其他用户分享 roles 。

#### 四、ansible部署

-  部署说明：ansible 只需要部署再一台机器上，通过主机清单，给需要控制的主机分组，通过ssh协议分组控制清单内的主机。



- 管理主机上使用pip install ansible 命令，或者 使用 yum install ansible。

- ansible 安装好了 ，使用命令看是否安装成功。

  有如下显示就说明已安装成功

  ```
  [root@localhost ~]# ansible --version
  ansible [core 2.11.6] 
    config file = /etc/ansible/ansible.cfg
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
    ansible python module location = /usr/local/python3/lib/python3.9/site-packages/ansible
    ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
    executable location = /usr/bin/ansible
    python version = 3.9.6 (default, Sep 10 2021, 00:23:01) [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
    jinja version = 3.0.2
    libyaml = True
  ```

  接下来需要配置ansible的主机清单文件和主配置文件。

  创建 /etc/ansible/ansible.cfg 和 /etc/ansible/hosts

- 配置ansible主机和被管主机的ssh连接。

```
# 服务端生成ssh key
ssh-keygen # 连续回车或者输入指定密码
# 拷贝ssh key到远程主机（被控主机），ssh的时候就不需要输入密码了 
# ssh-copy-id remoteuser@remoteserver 
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.8.188

#可以验证有没有成功，不再需要输入密码就配置成功了
ssh remoteuser@remoteserver
```



#### 五、ansible 多用户管理ansible

​	使用roles拆解playbook