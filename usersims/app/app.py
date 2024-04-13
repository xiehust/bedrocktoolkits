import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import pandas as pd

DAU = None
MAU = None
st.set_page_config(
    page_title="Claude 3 Pricing Simulator",
    page_icon="📊",
)
st.header("👋 Welcome to Claude 3 Pricing Simulator 📊",divider='rainbow')

st.subheader("一：用户参数模拟",divider='gray')
col1, col2 = st.columns(2)
with st.container():
    with col1:
        DAU = int( st.text_input('1. DAU,请输入日活用户如', 10000))
        min_rounds = int(st.text_input('3. 最小轮数,请输入最小轮数如,2', 2))
    with col2:
        MAU = int(st.text_input('2. MAU,请输入月活用户如', 50000))
        max_rounds = int(st.text_input('4. 最大轮数,请输入最大轮数如,200', 200))
        
    distribution_type = st.selectbox('选择用户聊天轮数分布类型', ['长尾分布','正态分布'])
    st.caption('长尾分布：一般常见于聊天，情感陪伴等。正态分布：一般常见于有固定用户引导模式，需要完成任务型，如教育类作文批改等')

    if distribution_type == '长尾分布':
        scale_factor = int(st.slider('选择系数，长尾分布为默认10，正态分布为2',0, 50, 10))

        if st.button('生成模拟数据',key='step0',type='primary'):
            t_rounds = np.round(np.random.exponential((scale_factor),(DAU)))
            t_rounds = np.clip(t_rounds, min_rounds, max_rounds)
            st.session_state['t_rounds'] = t_rounds
        if 't_rounds' in st.session_state:
            t_rounds = st.session_state['t_rounds']
            fig = ff.create_distplot(
                [t_rounds], ['rounds per user'], bin_size=[2])
            st.success('数据生成', icon="✅")
            st.plotly_chart(fig, use_container_width=True)
            st.write(pd.Series(t_rounds,name='轮数').describe())

    elif distribution_type == '正态分布':
        scale_factor = int(st.slider('选择系数，长尾分布为默认10，正太分布为2',0, 50, 2))
        expection =st.slider('选择正态分布的期望',0.0, 50.0, 20.0,0.5)
        if st.button('生成模拟数据',key='step1',type='primary'):
            t_rounds = np.round(np.random.normal(loc=expection, scale=scale_factor, size=(DAU)))
            t_rounds = np.clip(t_rounds, min_rounds, max_rounds)
            st.session_state['t_rounds'] = t_rounds
        if 't_rounds' in st.session_state:
            t_rounds = st.session_state['t_rounds']
            fig = ff.create_distplot(
                [t_rounds], ['rounds per user'], bin_size=[2])
            st.success('数据生成', icon="✅")
            st.plotly_chart(fig, use_container_width=True)
            st.write(pd.Series(t_rounds).describe())

st.divider() 
st.subheader("二：Token数模拟",divider='gray')
with st.container():
    st.markdown("""- 需要设定，Prompt模板的固定token数，多轮对话的时候，历史消息里只会放User实际Input，而不放Prompt template，所以需要分开计算"""
                """- 假设每轮的新消息的input token数和output token数是分别以E_In, E_Out 为期望的正态分布"""
                )
    fixed_prompt_template_token = int(st.text_input('用户Prompt提示词模板token数，包含system prompt', 1000))
    e_in = int(st.text_input('用户端实际输入的平均每轮token数', 500))
    scale_1 = int(st.slider('调整输入正态分布的系数(越大越窄)', 1,200,10))
    e_out = int(st.text_input('输出的平均每轮token数', 1000))
    scale_2 = int(st.slider('调整输出正态分布的系数(越大越窄)', 1,200,10))

    if st.button('生成模拟数据',key='step2',type='primary'):
        token_dist = np.random.normal(loc=(e_in,e_out), scale=[e_in/scale_1,e_out/scale_2], size=(DAU,2))
        token_dist = np.clip(np.round(token_dist.T),1,max(e_in,e_out)*4)
        st.session_state['token_dist'] = token_dist
    if 'token_dist' in st.session_state:
        token_dist = st.session_state['token_dist']
        fig = ff.create_distplot(
            token_dist, ['Input','Output'], bin_size=[2,2])
        st.success('数据生成', icon="✅")
        st.plotly_chart(fig, use_container_width=True)
        st.write(pd.DataFrame(token_dist.T,columns=['输入','输出']).describe())

    
st.divider() 
st.subheader("三：价格信息表",divider='gray')
with st.container():
    st.markdown(f"模型价格表-$每百万token")
    df = pd.DataFrame(
            [
            {"model": "haiku", "input_token_rate": 0.25, "output_token_rate": 1.25},
            {"model": "sonnet", "input_token_rate": 3, "output_token_rate": 15},
            {"model": "opus", "input_token_rate": 15, "output_token_rate": 75},
            {"model": "gpt-3.5", "input_token_rate": 0.5, "output_token_rate": 1.5},
            {"model": "gpt-4-turbo", "input_token_rate": 10, "output_token_rate": 30},
        ]
    ) 
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    def calc_rate(input_tokens,output_tokens,model):
        const_rate = 1/1e6
        df = edited_df[edited_df['model'] == model]
        in_token_rate = df['input_token_rate'].values[0]*const_rate
        out_token_rate = df['output_token_rate'].values[0]*const_rate
        return in_token_rate*input_tokens+out_token_rate*output_tokens



def is_data_ready():
    return True if 't_rounds' in st.session_state and 'token_dist' in st.session_state else False


st.divider() 
st.subheader("第四步：计算",divider='gray')
with st.container(): 
    # model_name = st.selectbox('选择模型', ['haiku', 'sonnet', 'opus','gpt-3.5','gpt-4-turbo'],key='11') 
    ##计算过程备注
    st.caption(
    """- **:blue[计算过程说明]** 
    - 每轮新对话发送给llm的输入input token = fixed_prompt_template_token + user_input_token + 历史消息的token. 
    - 一般历史消息里，只存放用户实际input token和output token，而fixed_prompt_template只会添加在当前的最新的对话里。 
    - 所以:第n轮对话的消耗token = (n-1)*(user_input_token+output_token) + (fixed_prompt_template_token + user_input_token+output_token)
    - 由于每轮对话，都会加上前N轮的对话记录，比如聊了n轮的用户，总共需要考虑的消息轮数，应该是1+2+3+...+n
    - 所以累加起来就是:
    """
    )
    st.latex("(user\_input\_token+output\_token) * \sum_{\mathclap{k=1}}^{n-1} k + n*(fixed\_prompt\_template\_token + user\_input\_token+output\_token)")
    st.latex("= (user\_input\_token+output\_token)*(1+n) * n/2 + n * fixed\_prompt\_template\_token")
    st.caption(
    """
    - 考虑有些场景最多保留前m轮历史消息， 当n>m时， 则实际消耗应该是: """)
    st.latex("(user\_input\_token+output\_token)* (\sum_{\mathclap{k=1}}^{m} k + (n-m)*m)+ n*fixed\_prompt\_template\_token" )
    st.caption("实际运算时，token, n,m 都会用(DAU)的数组代入，因此可以把上述公示拆解成3部分，直接进行批量运算，再加合")
    st.latex("\\tag{i} (1+m) * m/2* (user\_input\_token+output\_token)")
    st.latex("\\tag{ii} (n-m) * m * (user\_input\_token+output\_token)")
    st.latex("\\tag{iii} n * fixed\_prompt\_template\_token")
    st.caption(
        
    """最终三部分之和是总数( i + ii + iii )
    """) 
    
    st.markdown("**:blue[设置最大保留历史消息轮数]**")
    max_keep_turns = int(st.text_input('一次会话中，需要保留的最长消息轮数，例如最多前10轮', 10)) +1  ##加上新的一轮
    
    def compute(model_name):
        cliped_t_rounds = np.clip(t_rounds,min_rounds,max_keep_turns)
        pure_avg_cost_round = calc_rate(token_dist[0],token_dist[1],model=model_name)
        fixed_prompt_template_cost_round = calc_rate(fixed_prompt_template_token,0,model=model_name)


        rounds_part_1=  (1+cliped_t_rounds)*cliped_t_rounds /2 
        rounds_part_2= np.clip((t_rounds-cliped_t_rounds),0,t_rounds.max())*max_keep_turns  ##使用clip来确保只计算n>m的部分
        rounds_part_3 = t_rounds
        rounds_cost = rounds_part_1 * pure_avg_cost_round + rounds_part_2* pure_avg_cost_round + rounds_part_3*fixed_prompt_template_cost_round
        
        total_input_tokens =  rounds_part_1 *token_dist[0] + rounds_part_2*token_dist[0] + rounds_part_3*fixed_prompt_template_token
        total_output_tokens =  rounds_part_1 *token_dist[1] + rounds_part_2*token_dist[1]
        return rounds_cost, total_input_tokens, total_output_tokens
    
    results = []
    rounds_cost_list = {}
    if not is_data_ready():
        st.warning('请先生成模拟数据', icon="⚠️")
    if st.button('计算',key='step3',disabled = not is_data_ready(),type='primary'):
        st.session_state['step3_s'] = True
    if 'step3_s' in st.session_state:
        for model_name in list(edited_df['model'].values):
            rounds_cost, total_input_tokens, total_output_tokens = compute(model_name)
            rounds_cost_list = {**rounds_cost_list,model_name:rounds_cost}
            results.append({
                            "Model Name": model_name,
                            # "总轮数 每天": t_rounds.sum()/1000,
                            "总input token 每天(k)":round(total_input_tokens.sum()/1000),
                            "总output token 每天(k)":round(total_output_tokens.sum()/1000),
                            "总cost 每天($)": round(rounds_cost.sum()),
                            "总cost 每月($)": round(rounds_cost.sum()*30),
                            "每月用户cost/MAU 成本($) ": round(rounds_cost.sum()*30/MAU,2),
                           })
        st.session_state['rounds_cost_list'] = rounds_cost_list
        # st.markdown("**:blue[计算结果]**")
        st.success('计算结果', icon="✅")
        st.table(pd.DataFrame(results))

st.divider() 
st.subheader("按用户的轮数分层，看各层的cost占比",divider='gray')
with st.container(): 
    model_name_view = st.selectbox('选择模型', ['haiku', 'sonnet', 'opus','gpt-3.5','gpt-4-turbo'],key='22') 
    if not is_data_ready():
        st.warning('请先生成模拟数据', icon="⚠️")
    if st.button('查看',key='step4', disabled = not is_data_ready(),type='primary'):
        if 'rounds_cost_list' in st.session_state:
            rounds_cost_view = st.session_state.rounds_cost_list.get(model_name_view)
            rounds_cost_view= pd.Series(rounds_cost_view)
            cost_pct = []
            total = rounds_cost_view.sum()
            for q in np.arange(0,1,0.1):
                b = rounds_cost_view.quantile(q)
                cost_pct.append([q,rounds_cost_view[rounds_cost_view>=b].sum()/total])    
            data = pd.DataFrame(cost_pct,columns=['百分位','Cost占比'])
            st.success('分层数据', icon="✅")
            st.table(data)

st.divider() 
st.markdown(
 """
    **:red[免责说明]**
    - 本计算器仅利用概率分布来拟合并模拟用户行为，通过这些生成的数据来模拟不同条件下使用Claude 3系列模型产生的费用
    - 本计算器的仅用于模拟测算，结果仅供参考，请勿用于实际报价
"""
)
