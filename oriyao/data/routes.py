from oriyao import mongo
from oriyao.data import blueprint
from flask import current_app,render_template
from flask_login import login_required

from pyecharts import options as opts
from pyecharts.charts import Bar
import time,datetime

@blueprint.route('/statistics/')
def statistics():
    days = []
    vst_data = []
    cst_data = []
    lst_data = []
    
    collection_statistics = mongo.db['statistics']
    
    # Query 7 days data
    condition = {'date':{"$gte":(datetime.date.today() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")}}

    statistics = collection_statistics.find(condition).sort('date',1)

    for sta in statistics:
        current_app.logger.warning(sta)
        days.append(str(sta['date']))       
       	vst_data.append(str(sta['visitstatistics']))
        cst_data.append(str(sta['commentstatistics']))
        lst_data.append(str(sta['likestatistics']))

    bar = (
        Bar()
            .add_xaxis(days)
            .add_yaxis("访问", vst_data)
            .add_yaxis("评论", cst_data)
            .add_yaxis("点赞", lst_data)
            .set_global_opts(title_opts=opts.TitleOpts(title="网站统计", subtitle="今日数据"))
    )
    return render_template('statistics.html',bar_options=bar.dump_options())


@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')
