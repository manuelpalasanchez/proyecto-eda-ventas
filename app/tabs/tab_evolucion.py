import streamlit as st
import plotly.express as px

def render(df_filtrado):
    col1, col2 = st.columns(2)

    with col1:
        profit_anual = df_filtrado.groupby('Year')['Profit'].sum().reset_index()

        fig = px.line(
            profit_anual,
            x='Year',
            y='Profit',
            markers=True,
            title='Evolución del profit anual',
            labels={'Year': 'Año', 'Profit': 'Profit total'}
        )
        fig.update_traces(line_color='steelblue', marker_size=8)
        st.plotly_chart(fig, width='stretch')

    with col2:
        profit_year_cat = df_filtrado.groupby(['Year', 'Category'])['Profit'].sum().reset_index()

        fig2 = px.line(
            profit_year_cat,
            x='Year',
            y='Profit',
            color='Category',
            markers=True,
            title='Profit anual por categoría',
            labels={'Year': 'Año', 'Profit': 'Profit total'}
        )
        st.plotly_chart(fig2, width='stretch')

    st.markdown("---")
    st.markdown("Desglose de rentabilidad por subcategoría para cada año seleccionado.")
    años = sorted(df_filtrado['Year'].unique())
    cols = st.columns(min(2, len(años)))

    for i, year in enumerate(años):
        data = df_filtrado[df_filtrado['Year'] == year].groupby('Sub-Category')['Profit'].sum().reset_index()
        data = data.sort_values('Profit')
        data['color'] = data['Profit'].apply(lambda x: 'Pérdidas' if x < 0 else 'Beneficios')

        fig = px.bar(
            data,
            x='Profit',
            y='Sub-Category',
            orientation='h',
            color='color',
            color_discrete_map={'Beneficios': 'steelblue', 'Pérdidas': 'crimson'},
            title=f'Profit por subcategoría — {year}'
        )
        fig.add_vline(x=0, line_color='black', line_width=1)
        fig.update_layout(showlegend=False)
        cols[i % 2].plotly_chart(fig, width='stretch')