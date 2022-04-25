from django.db import models

# Create your models here.
class Board(models.Model):
    # packet의 데이터 타입들
    idx = models.AutoField(primary_key=True, verbose_name="ID")
    localtime = models.CharField(null=True,max_length=128,
                            verbose_name='local_time')
    protoT = models.CharField(max_length=128,
                            verbose_name='proto_T')
    layerv = models.CharField(max_length=128,
                            verbose_name='layer_V')
    srcip = models.CharField(max_length=128,
                            verbose_name='src_ip')
    srcport = models.CharField(max_length=128,
                            verbose_name='src_port')
    dstip = models.CharField(max_length=128,
                            verbose_name='dst_ip', null=True)
    dstport = models.CharField(max_length=128,
                            verbose_name='dst_port', null=True)
    pktsize = models.CharField(max_length=128,
                            verbose_name='pkt_size', null=True)
    '''
    # ip의 데이터 타입들 -> db까지 안해도 되겠다 싶어서 주석처리해놓음
    # id, ip, 노드실제위치, 발생하는 트래픽값, 토르사용유무, 가장 인접한 노드 이름
    # id, ip, NodeLocaton, Traffic_var, toruse, nearnode
    idx = models.AutoField(primary_key=True, verbose_name="ID")
    ip = models.CharField(null=True,max_length=128,
                            verbose_name='IP')
    nodelocation = models.CharField(max_length=128,
                            verbose_name='Node_Location')
    trafficvar = models.CharField(max_length=128,
                            verbose_name='Traffic_var')
    toruse = models.CharField(max_length=128,
                            verbose_name='Tor_Use')
    nearnode = models.CharField(max_length=128,
                            verbose_name='Near_Node')
    '''
    
    def __str__(self):
        return self.idx

    class Meta:
        db_table = 'capstone_board'
        verbose_name = 'zeronet_packet'
        verbose_name_plural = 'zeronet_packet'