import streamlit as st
import plotly.express as px

def render(df_filtrado):
    st.markdown("Visión general de la rentabilidad por categoría y región.")
    col1, col2 = st.columns(2)

    with col1:
        profit_cat = df_filtrado.groupby('Category')['Profit'].sum().reset_index()
        profit_cat = profit_cat.sort_values('Profit')
        profit_cat['color'] = profit_cat['Profit'].apply(lambda x: 'Pérdidas' if x < 0 else 'Beneficios')

        fig = px.bar(
            profit_cat,
            x='Profit',
            y='Category',
            orientation='h',
            color='color',
            color_discrete_map={'Beneficios': 'steelblue', 'Pérdidas': 'crimson'},
            title='Profit total por categoría'
        )
        fig.add_vline(x=0, line_color='black', line_width=1)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width='stretch')

    with col2:
        profit_reg = df_filtrado.groupby('Region').agg(
            Profit_Total=('Profit', 'sum'),
            Profit_Medio=('Profit', 'mean')
        ).reset_index().sort_values('Profit_Total')

        fig2 = px.bar(
            profit_reg,
            x='Profit_Total',
            y='Region',
            orientation='h',
            color='Profit_Total',
            color_discrete_sequence=['steelblue'],
            title='Profit total por región',
            hover_data={'Profit_Medio': ':.2f'}
        )
        fig2.add_vline(x=0, line_color='black', line_width=1)
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, width='stretch')
    st.markdown("---")
    profit_subcat_general = df_filtrado.groupby('Sub-Category')['Profit'].sum().reset_index()
    profit_subcat_general = profit_subcat_general.sort_values('Profit')
    profit_subcat_general['color'] = profit_subcat_general['Profit'].apply(lambda x: 'Pérdidas' if x < 0 else 'Beneficios')

    fig3 = px.bar(
        profit_subcat_general,
        x='Profit',
        y='Sub-Category',
        orientation='h',
        color='color',
        color_discrete_map={'Beneficios': 'steelblue', 'Pérdidas': 'crimson'},
        title='Profit total por subcategoría'
    )
    fig3.add_vline(x=0, line_color='black', line_width=1)
    fig3.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig3, width='stretch')
