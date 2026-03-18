import streamlit as st
import plotly.express as px

def render(df_filtrado):
    st.markdown("Subcategorías con pérdidas sistemáticas e impacto de los descuentos en la rentabilidad.")
    col1, col2 = st.columns(2)

    with col1:
        profit_subcat = df_filtrado.groupby('Sub-Category')['Profit'].sum().reset_index()
        profit_subcat = profit_subcat.sort_values('Profit')
        profit_subcat['color'] = profit_subcat['Profit'].apply(lambda x: 'Pérdidas' if x < 0 else 'Beneficios')

        fig = px.bar(
            profit_subcat,
            x='Profit',
            y='Sub-Category',
            orientation='h',
            color='color',
            color_discrete_map={'Beneficios': 'steelblue', 'Pérdidas': 'crimson'},
            title='Profit total por subcategoría'
        )
        fig.add_vline(x=0, line_color='black', line_width=1)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width='stretch')

    with col2:
        fig2 = px.scatter(
            df_filtrado,
            x='Discount',
            y='Profit',
            opacity=0.4,
            color='Category',
            title='Descuento vs Profit por transacción',
            labels={'Discount': 'Descuento', 'Profit': 'Profit'}
        )
        fig2.add_hline(y=0, line_color='red', line_dash='dash')
        fig2.add_vline(x=0.2, line_color='orange', line_dash='dash',
                       annotation_text='20% umbral', annotation_position='top right')
        st.plotly_chart(fig2, width='stretch')