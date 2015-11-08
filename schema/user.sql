create database `user` default charset utf8mb4;
grant select,insert,update,delete on `user`.* to root@'%' identified by 'qweasd';
use `user`;

-- 用户表
-- username 4～30 中文字母数字
-- 默认可以不填，都转换成简体，小写再保存
-- 如果转换后不一样，data里冗余一份原始的
create table `user` (
    id integer unsigned not null auto_increment,
    username varchar(128) charset utf8mb4 collate utf8mb4_general_ci default null,
    data varchar(4096) not null,
    status integer unsigned not null,
    create_time datetime not null,
    primary key (id),
    unique key uniq_username(username)
) Engine=InnoDB ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=4;

-- 登录信息
create table user_passport (
    id integer unsigned not null,
    account varchar(64) character set latin1 not null collate latin1_general_ci,
    password varchar(127) character set latin1 not null collate latin1_bin,
    status integer unsigned not null,
    update_time bigint unsigned not null,
    create_time datetime not null,
    primary key (id),
    unique key uniq_number(account)
) Engine=InnoDB;

-- 票
-- create_time 会用作salt
create table ticket (
    id bigint unsigned not null auto_increment,
    user_id integer unsigned not null,
    create_time bigint unsigned not null,
    primary key (id),
    unique key uniq_userid(user_id)
) Engine=InnoDB;
