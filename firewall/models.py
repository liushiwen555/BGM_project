from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from utils.helper import random_string

# Create your models here.
from utils.validators import MAC_VALIDATOR

REGISTER_CODE_LEN = 8
ACTION_DENY = 0
ACTION_PERMIT = 1
ACTION_CHOICES = (
    (ACTION_DENY, '拒绝'),
    (ACTION_PERMIT, '允许'),
)

STATUS_DISABLE = 0
STATUS_ENABLE = 1
STATUS_CHOICES = (
    (STATUS_DISABLE, '关闭'),
    (STATUS_ENABLE, '开启'),
)

LOGGING_OFF = 0
LOGGING_ON = 1
LOGGING_CHOICES = (
    (LOGGING_OFF, '关闭'),
    (LOGGING_ON, '开启'),
)


class Firewall(models.Model):

    ONLINE = 1
    OFFLINE = 2
    NOT_REGISTERED = 3
    STATUS_CHOICES = (
        (ONLINE, '在线'),
        (OFFLINE, '离线'),
        (NOT_REGISTERED, '未注册'),
    )

    dev_code = models.CharField('设备编号', max_length=32)
    dev_name = models.CharField('设备名', max_length=20)
    dev_location = models.CharField('设备位置', max_length=20)
    ip = models.GenericIPAddressField('ip', unique=True, null=True)
    version = models.CharField('版本号', max_length=20, null=True)
    responsible_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='责任人')
    register_code = models.CharField('注册码', max_length=20)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=NOT_REGISTERED)
    registered_time = models.DateTimeField('注册时间', null=True)

    class Meta:
        verbose_name = '防火墙设备'

    def __str__(self):
        return '{} {}'.format(self.id, self.dev_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 要在添加防火墙时生成一个注册码
        self.register_code = random_string(REGISTER_CODE_LEN)
        super(Firewall, self).save(force_insert, force_update, using, update_fields)


class BaseStrategy(models.Model):

    strategy_name = models.CharField(max_length=32)
    created_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_time',)


class ConfStrategy(BaseStrategy):

    RUN_MODE_TEST = 0
    RUN_MODE_WORKING = 1
    RUN_MODE_CHOICES = (
        (RUN_MODE_TEST, '测试模式'),
        (RUN_MODE_WORKING, '离线'),
    )

    DEFAULT_FILTER_ON = 0
    DEFAULT_FILTER_OFF = 1
    DEFAULT_FILTER_CHOICES = (
        (DEFAULT_FILTER_ON, '开启'),
        (DEFAULT_FILTER_OFF, '关闭'),
    )

    DPI_ON = 0
    DPI_OFF = 1
    DPI_CHOICES = (
        (DPI_ON, '开启'),
        (DPI_OFF, '关闭'),
    )

    run_mode = models.IntegerField('运行模式', choices=RUN_MODE_CHOICES)
    default_filter = models.IntegerField('默认禁止', choices=DEFAULT_FILTER_CHOICES)
    DPI = models.IntegerField('深度检测', choices=DPI_CHOICES)


class BaseFirewallStrategy(BaseStrategy):

    rule_id = models.IntegerField('规则ID', unique=True)
    rule_name = models.CharField('规则名称', max_length=64)
    src_ip = models.GenericIPAddressField('源ip')
    dst_ip = models.GenericIPAddressField('目的ip')
    src_port = models.IntegerField('源端口', null=True, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    dst_port = models.IntegerField('目的端口', null=True, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    protocol = models.CharField('协议', max_length=32, blank=True, null=True)
    action = models.IntegerField('动作', choices=ACTION_CHOICES)
    status = models.IntegerField('状态', choices=STATUS_CHOICES)


class WhiteListStrategy(BaseStrategy):

    rule_id = models.IntegerField('规则ID', unique=True)
    rule_name = models.CharField('规则名称', max_length=64)
    src_ip = models.GenericIPAddressField('源ip')
    dst_ip = models.GenericIPAddressField('目的ip')
    src_port = models.IntegerField('源端口', null=True, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    dst_port = models.IntegerField('目的端口', null=True, validators=[MinValueValidator(1), MaxValueValidator(65535)])
    protocol = models.CharField('协议', max_length=32, blank=True, null=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES)
    logging = models.IntegerField('记录日志', choices=LOGGING_CHOICES)


class IndustryProtocolStrategy(BaseStrategy):

    pass


class IndustryProtocolDefaultConfStrategy(IndustryProtocolStrategy):

    OPC_default_action = models.IntegerField('OPC-DA默认动作', choices=STATUS_CHOICES)
    modbus_default_action = models.IntegerField('modbus默认动作', choices=STATUS_CHOICES)


class IndustryProtocolCustomConfStrategy(IndustryProtocolStrategy):

    READ_WRITE_ACTION_PASS = 1
    READ_WRITE_ACTION_WARNING = 2
    READ_WRITE_ACTION_DROP = 3
    READ_WRITE_ACTION_BLOCK = 4

    READ_WRITE_ACTION_CHOICES = (
        (READ_WRITE_ACTION_PASS, '通过'),
        (READ_WRITE_ACTION_WARNING, '告警'),
        (READ_WRITE_ACTION_DROP, '丢弃'),
        (READ_WRITE_ACTION_BLOCK, '阻断'),
    )
    is_read_open = models.BooleanField('写入开关', default=False)
    read_action = models.IntegerField('写入事件处理', choices=READ_WRITE_ACTION_CHOICES)
    is_write_open = models.BooleanField('读取开关', default=False)
    write_action = models.IntegerField('读取事件处理', choices=READ_WRITE_ACTION_CHOICES)


class IndustryProtocolModbusStrategy(IndustryProtocolStrategy):

    rule_id = models.IntegerField('规则ID', unique=True)
    rule_name = models.CharField('规则名称', max_length=64)
    func_code = models.CharField('功能码', max_length=64)
    reg_start = models.CharField('开始地址', max_length=64)
    reg_end = models.CharField('结束地址', max_length=64)
    reg_value = models.CharField('寄存器值', max_length=64)
    length = models.IntegerField('长度')
    action = models.IntegerField('动作', choices=ACTION_CHOICES)
    logging = models.IntegerField('记录日志', choices=LOGGING_CHOICES)


class IndustryProtocolS7Strategy(IndustryProtocolStrategy):

    rule_id = models.IntegerField('规则ID', unique=True)
    rule_name = models.CharField('规则名称', max_length=64)
    functype = models.CharField('Function type', max_length=64)
    pdu_type = models.CharField('pdu type', max_length=64)
    action = models.IntegerField('动作', choices=ACTION_CHOICES)
    status = models.IntegerField('状态', choices=STATUS_CHOICES)


class BlackListStrategy(BaseStrategy):

    LEVEL_LOW = 1
    LEVEL_MEDIUM = 1
    LEVEL_HIGH = 1

    LEVEL_CHOICE = (
        (LEVEL_LOW, '低'),
        (LEVEL_MEDIUM, '中'),
        (LEVEL_HIGH, '高'),
    )
    
    EVENT_PROCESS_PASS = 1
    EVENT_PROCESS_WARNING = 2
    EVENT_PROCESS_DROP = 3
    EVENT_PROCESS_BLOCK = 4

    EVENT_PROCESS_CHOICES = (
        (EVENT_PROCESS_PASS, '通过'),
        (EVENT_PROCESS_WARNING, '告警'),
        (EVENT_PROCESS_DROP, '丢弃'),
        (EVENT_PROCESS_BLOCK, '阻断'),
    )

    vulnerability_name = models.CharField('漏洞名称', max_length=1000)
    publish_time = models.DateTimeField('发布时间')
    level = models.IntegerField('风险等级')
    event_process = models.IntegerField('事件处理', choices=EVENT_PROCESS_CHOICES)
    content = models.CharField('内容', max_length=10000)
    status = models.IntegerField('启用状态', choices=STATUS_CHOICES)


class IPMacBind(BaseStrategy):
    manufacturer = models.CharField('设备厂商', max_length=64)
    ip = models.GenericIPAddressField('ip')
    mac = models.CharField('mac', validators=[MAC_VALIDATOR], max_length=32)
    status = models.IntegerField('启用状态', choices=STATUS_CHOICES)

    class Meta:
        ordering = ('-created_time',)
        unique_together = ('ip', 'mac',)


class SecEvent(models.Model):
    
    STATUS_WARNING = 1
    STATUS_DROP = 2
    STATUS_BLOCK = 3

    STATUS_CHOICES = (
        (STATUS_WARNING, '告警'),
        (STATUS_DROP, '丢弃'),
        (STATUS_BLOCK, '阻断'),
    )

    RISK_LEVEL_LOW = 0
    RISK_LEVEL_MEDIUM = 1
    RISK_LEVEL_HIGH = 2

    RISK_LEVEL_CHOICES = (
        (RISK_LEVEL_LOW, '低'),
        (RISK_LEVEL_MEDIUM, '中'),
        (RISK_LEVEL_HIGH, '高'),
    )

    ACTION_UNREAD = 0
    ACTION_READ = 1
    READ_ACTION_CHOICES = (
        (ACTION_UNREAD, '未读'),
        (ACTION_READ, '已读'),
    )

    src_ip = models.GenericIPAddressField('源地址')
    dst_ip = models.GenericIPAddressField('目的地址')
    protocol = models.CharField('协议', max_length=32, blank=True, null=True)
    occurred_time = models.DateTimeField('时间', auto_now_add=True)
    status = models.IntegerField('事件登记', choices=STATUS_CHOICES)
    risk_level = models.IntegerField('风险登记', choices=RISK_LEVEL_CHOICES)
    action = models.IntegerField('状态', choices=READ_ACTION_CHOICES)
    rule_id = models.IntegerField('规则ID')


class SysEvent(models.Model):

    LEVEL_MESSAGE = 0
    LEVEL_WARNING = 1
    LEVEL_MESSAGE_AND_WARNING = 3

    LEVEL_CHOICES = (
        (LEVEL_MESSAGE, '信息'),
        (LEVEL_WARNING, '告警'),
        (LEVEL_MESSAGE_AND_WARNING, '信息和告警'),
    )

    EVENT_TYPE_DEVICE_STATUS = 0
    EVENT_TYPE_INTERFACE_STATUS = 1
    EVENT_TYPE_DATA_COLLECT = 10
    EVENT_TYPE_DISK_CLEAN = 11
    EVENT_TYPE_WHITELIST = 12
    EVENT_TYPE_BLACKLIST = 13
    EVENT_TYPE_IP_MAC = 14
    EVENT_TYPE_NO_FLOW = 15
    EVENT_TYPE_BASE_FIREWALL = 19
    EVENT_TYPE_CUSTOM_WHITELIST = 20
    EVENT_TYPE_SESSION_MANAGEMENT = 21
    EVENT_TYPE_INDUSTRY_PROTOCOL = 22

    EVENT_TYPE_CHOICES = (
        (EVENT_TYPE_DEVICE_STATUS, '设备状态'),
        (EVENT_TYPE_INTERFACE_STATUS, '接口状态'),
        (EVENT_TYPE_DATA_COLLECT, '数据采集'),
        (EVENT_TYPE_DISK_CLEAN, '磁盘清理'),
        (EVENT_TYPE_WHITELIST, '白名单'),
        (EVENT_TYPE_BLACKLIST, '黑名单'),
        (EVENT_TYPE_IP_MAC, 'IP MAC'),
        (EVENT_TYPE_NO_FLOW, '无流量监测'),
        (EVENT_TYPE_CUSTOM_WHITELIST, '自定义白名单'),
        (EVENT_TYPE_SESSION_MANAGEMENT, '连接管理'),
        (EVENT_TYPE_INDUSTRY_PROTOCOL, '工业协议'),
    )

    level = models.IntegerField('事件等级', choices=LEVEL_CHOICES)
    event_type = models.IntegerField('事件类型', choices=EVENT_TYPE_CHOICES)
    content = models.CharField('内容', max_length=10000)
    occurred_time = models.DateTimeField('时间')
    status = models.IntegerField('事件状态', choices=STATUS_CHOICES)
