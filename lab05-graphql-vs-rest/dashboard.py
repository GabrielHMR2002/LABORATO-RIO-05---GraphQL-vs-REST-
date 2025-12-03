"""
Dashboard de Visualização: GraphQL vs REST
Disciplina: Laboratório de Experimentação de Software
Curso: Engenharia de Software
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Configurações
INPUT_DIR = "results"
INPUT_FILE = "experiment_results.csv"
OUTPUT_DIR = "results/graficos"

# Configurações de estilo
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {'REST': '#3498db', 'GraphQL': '#e74c3c'}
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# ============================================
# CARREGAR DADOS
# ============================================

def load_data():
    """Carrega os dados do experimento"""
    filepath = os.path.join(INPUT_DIR, INPUT_FILE)
    
    if not os.path.exists(filepath):
        print(f"ERRO: Arquivo não encontrado: {filepath}")
        print("Execute primeiro: python experimento.py")
        exit(1)
    
    df = pd.read_csv(filepath)
    print(f"Dados carregados: {len(df)} registros\n")
    return df

def setup_output_dir():
    """Cria diretório de saída se não existir"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Diretório criado: {OUTPUT_DIR}\n")

# ============================================
# GRÁFICO 1: BOXPLOT - TEMPO DE RESPOSTA
# ============================================

def plot_time_boxplot(df):
    """Boxplot comparando tempo de resposta"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Boxplot geral
    sns.boxplot(data=df, x='api_type', y='time_ms', ax=axes[0],
                palette=COLORS, order=['REST', 'GraphQL'])
    axes[0].set_title('RQ1: Tempo de Resposta - REST vs GraphQL', fontweight='bold')
    axes[0].set_xlabel('Tipo de API')
    axes[0].set_ylabel('Tempo (ms)')
    
    # Adicionar médias
    means = df.groupby('api_type')['time_ms'].mean()
    for i, api in enumerate(['REST', 'GraphQL']):
        axes[0].annotate(f'μ = {means[api]:.1f}ms',
                         xy=(i, means[api]),
                         xytext=(i + 0.25, means[api]),
                         fontsize=10, fontweight='bold')
    
    # Boxplot por complexidade
    sns.boxplot(data=df, x='complexity', y='time_ms', hue='api_type',
                ax=axes[1], palette=COLORS, hue_order=['REST', 'GraphQL'],
                order=['simple', 'medium', 'complex'])
    axes[1].set_title('Tempo de Resposta por Complexidade', fontweight='bold')
    axes[1].set_xlabel('Complexidade da Consulta')
    axes[1].set_ylabel('Tempo (ms)')
    axes[1].legend(title='API')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '01_tempo_boxplot.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GRÁFICO 2: BOXPLOT - TAMANHO DA RESPOSTA
# ============================================

def plot_size_boxplot(df):
    """Boxplot comparando tamanho das respostas"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Boxplot geral
    sns.boxplot(data=df, x='api_type', y='size_bytes', ax=axes[0],
                palette=COLORS, order=['REST', 'GraphQL'])
    axes[0].set_title('RQ2: Tamanho da Resposta - REST vs GraphQL', fontweight='bold')
    axes[0].set_xlabel('Tipo de API')
    axes[0].set_ylabel('Tamanho (bytes)')
    
    # Adicionar médias
    means = df.groupby('api_type')['size_bytes'].mean()
    for i, api in enumerate(['REST', 'GraphQL']):
        axes[0].annotate(f'μ = {means[api]:.0f}B',
                         xy=(i, means[api]),
                         xytext=(i + 0.25, means[api]),
                         fontsize=10, fontweight='bold')
    
    # Boxplot por complexidade
    sns.boxplot(data=df, x='complexity', y='size_bytes', hue='api_type',
                ax=axes[1], palette=COLORS, hue_order=['REST', 'GraphQL'],
                order=['simple', 'medium', 'complex'])
    axes[1].set_title('Tamanho da Resposta por Complexidade', fontweight='bold')
    axes[1].set_xlabel('Complexidade da Consulta')
    axes[1].set_ylabel('Tamanho (bytes)')
    axes[1].legend(title='API')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '02_tamanho_boxplot.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GRÁFICO 3: DISTRIBUIÇÕES (HISTOGRAMAS)
# ============================================

def plot_distributions(df):
    """Histogramas e KDE das distribuições"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Tempo - REST
    sns.histplot(df[df['api_type'] == 'REST']['time_ms'], kde=True,
                 ax=axes[0, 0], color=COLORS['REST'], bins=30)
    axes[0, 0].set_title('Distribuição Tempo - REST', fontweight='bold')
    axes[0, 0].set_xlabel('Tempo (ms)')
    axes[0, 0].set_ylabel('Frequência')
    
    # Tempo - GraphQL
    sns.histplot(df[df['api_type'] == 'GraphQL']['time_ms'], kde=True,
                 ax=axes[0, 1], color=COLORS['GraphQL'], bins=30)
    axes[0, 1].set_title('Distribuição Tempo - GraphQL', fontweight='bold')
    axes[0, 1].set_xlabel('Tempo (ms)')
    axes[0, 1].set_ylabel('Frequência')
    
    # Tamanho - REST
    sns.histplot(df[df['api_type'] == 'REST']['size_bytes'], kde=True,
                 ax=axes[1, 0], color=COLORS['REST'], bins=30)
    axes[1, 0].set_title('Distribuição Tamanho - REST', fontweight='bold')
    axes[1, 0].set_xlabel('Tamanho (bytes)')
    axes[1, 0].set_ylabel('Frequência')
    
    # Tamanho - GraphQL
    sns.histplot(df[df['api_type'] == 'GraphQL']['size_bytes'], kde=True,
                 ax=axes[1, 1], color=COLORS['GraphQL'], bins=30)
    axes[1, 1].set_title('Distribuição Tamanho - GraphQL', fontweight='bold')
    axes[1, 1].set_xlabel('Tamanho (bytes)')
    axes[1, 1].set_ylabel('Frequência')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '03_distribuicoes.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GRÁFICO 4: BARRAS COM INTERVALO DE CONFIANÇA
# ============================================

def plot_bar_ci(df):
    """Gráfico de barras com intervalo de confiança 95%"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Tempo por complexidade
    sns.barplot(data=df, x='complexity', y='time_ms', hue='api_type',
                ax=axes[0], palette=COLORS, hue_order=['REST', 'GraphQL'],
                order=['simple', 'medium', 'complex'],
                errorbar=('ci', 95), capsize=0.1)
    axes[0].set_title('Tempo Médio de Resposta (IC 95%)', fontweight='bold')
    axes[0].set_xlabel('Complexidade')
    axes[0].set_ylabel('Tempo (ms)')
    axes[0].legend(title='API')
    
    # Tamanho por complexidade
    sns.barplot(data=df, x='complexity', y='size_bytes', hue='api_type',
                ax=axes[1], palette=COLORS, hue_order=['REST', 'GraphQL'],
                order=['simple', 'medium', 'complex'],
                errorbar=('ci', 95), capsize=0.1)
    axes[1].set_title('Tamanho Médio da Resposta (IC 95%)', fontweight='bold')
    axes[1].set_xlabel('Complexidade')
    axes[1].set_ylabel('Tamanho (bytes)')
    axes[1].legend(title='API')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '04_barras_ic95.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GRÁFICO 5: VIOLIN PLOT
# ============================================

def plot_violin(df):
    """Violin plots para visualização completa da distribuição"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    sns.violinplot(data=df, x='complexity', y='time_ms', hue='api_type',
                   split=True, ax=axes[0], palette=COLORS,
                   hue_order=['REST', 'GraphQL'],
                   order=['simple', 'medium', 'complex'])
    axes[0].set_title('Distribuição do Tempo de Resposta', fontweight='bold')
    axes[0].set_xlabel('Complexidade')
    axes[0].set_ylabel('Tempo (ms)')
    axes[0].legend(title='API')
    
    sns.violinplot(data=df, x='complexity', y='size_bytes', hue='api_type',
                   split=True, ax=axes[1], palette=COLORS,
                   hue_order=['REST', 'GraphQL'],
                   order=['simple', 'medium', 'complex'])
    axes[1].set_title('Distribuição do Tamanho da Resposta', fontweight='bold')
    axes[1].set_xlabel('Complexidade')
    axes[1].set_ylabel('Tamanho (bytes)')
    axes[1].legend(title='API')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '05_violin.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GRÁFICO 6: HEATMAP POR REPOSITÓRIO
# ============================================

def plot_heatmap(df):
    """Heatmaps das métricas por repositório"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 10))
    
    # Preparar dados para tempo
    pivot_time = df.pivot_table(
        values='time_ms',
        index='repository',
        columns=['api_type', 'complexity'],
        aggfunc='mean'
    ).round(1)
    
    # Reordenar colunas
    cols_order = [('REST', 'simple'), ('GraphQL', 'simple'),
                  ('REST', 'medium'), ('GraphQL', 'medium'),
                  ('REST', 'complex'), ('GraphQL', 'complex')]
    pivot_time = pivot_time[[c for c in cols_order if c in pivot_time.columns]]
    
    sns.heatmap(pivot_time, annot=True, fmt='.0f', cmap='RdYlGn_r',
                ax=axes[0], cbar_kws={'label': 'Tempo (ms)'})
    axes[0].set_title('Tempo Médio por Repositório (ms)', fontweight='bold')
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Repositório')
    
    # Preparar dados para tamanho
    pivot_size = df.pivot_table(
        values='size_bytes',
        index='repository',
        columns=['api_type', 'complexity'],
        aggfunc='mean'
    ).round(0)
    
    pivot_size = pivot_size[[c for c in cols_order if c in pivot_size.columns]]
    
    sns.heatmap(pivot_size, annot=True, fmt='.0f', cmap='RdYlGn_r',
                ax=axes[1], cbar_kws={'label': 'Tamanho (bytes)'})
    axes[1].set_title('Tamanho Médio por Repositório (bytes)', fontweight='bold')
    axes[1].set_xlabel('')
    axes[1].set_ylabel('Repositório')
    
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '06_heatmap.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GRÁFICO 7: COMPARATIVO GERAL
# ============================================

def plot_summary(df):
    """Gráfico resumo com comparativo geral"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Média geral - Tempo
    time_means = df.groupby('api_type')['time_ms'].mean()
    bars1 = axes[0, 0].bar(['REST', 'GraphQL'], 
                           [time_means['REST'], time_means['GraphQL']],
                           color=[COLORS['REST'], COLORS['GraphQL']])
    axes[0, 0].set_title('Tempo Médio de Resposta', fontweight='bold')
    axes[0, 0].set_ylabel('Tempo (ms)')
    axes[0, 0].bar_label(bars1, fmt='%.1f ms')
    
    # 2. Média geral - Tamanho
    size_means = df.groupby('api_type')['size_bytes'].mean()
    bars2 = axes[0, 1].bar(['REST', 'GraphQL'],
                           [size_means['REST'], size_means['GraphQL']],
                           color=[COLORS['REST'], COLORS['GraphQL']])
    axes[0, 1].set_title('Tamanho Médio da Resposta', fontweight='bold')
    axes[0, 1].set_ylabel('Tamanho (bytes)')
    axes[0, 1].bar_label(bars2, fmt='%.0f B')
    
    # 3. Diferença percentual por complexidade - Tempo
    complexities = ['simple', 'medium', 'complex']
    diff_time = []
    for c in complexities:
        rest = df[(df['api_type'] == 'REST') & (df['complexity'] == c)]['time_ms'].mean()
        gql = df[(df['api_type'] == 'GraphQL') & (df['complexity'] == c)]['time_ms'].mean()
        diff_time.append(((rest - gql) / rest) * 100)
    
    colors_diff = ['green' if d > 0 else 'red' for d in diff_time]
    bars3 = axes[1, 0].bar(complexities, diff_time, color=colors_diff)
    axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    axes[1, 0].set_title('Diferença de Tempo: REST vs GraphQL', fontweight='bold')
    axes[1, 0].set_ylabel('Diferença (%)')
    axes[1, 0].set_xlabel('Complexidade')
    axes[1, 0].bar_label(bars3, fmt='%.1f%%')
    
    # 4. Diferença percentual por complexidade - Tamanho
    diff_size = []
    for c in complexities:
        rest = df[(df['api_type'] == 'REST') & (df['complexity'] == c)]['size_bytes'].mean()
        gql = df[(df['api_type'] == 'GraphQL') & (df['complexity'] == c)]['size_bytes'].mean()
        diff_size.append(((rest - gql) / rest) * 100)
    
    colors_diff2 = ['green' if d > 0 else 'red' for d in diff_size]
    bars4 = axes[1, 1].bar(complexities, diff_size, color=colors_diff2)
    axes[1, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    axes[1, 1].set_title('Diferença de Tamanho: REST vs GraphQL', fontweight='bold')
    axes[1, 1].set_ylabel('Diferença (%)')
    axes[1, 1].set_xlabel('Complexidade')
    axes[1, 1].bar_label(bars4, fmt='%.1f%%')
    
    plt.suptitle('Resumo Comparativo: GraphQL vs REST', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, '07_resumo_comparativo.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# TABELA RESUMO
# ============================================

def create_summary_table(df):
    """Cria tabela resumo visual"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    
    # Calcular estatísticas
    summary_data = []
    for api in ['REST', 'GraphQL']:
        for comp in ['simple', 'medium', 'complex']:
            subset = df[(df['api_type'] == api) & (df['complexity'] == comp)]
            summary_data.append([
                api,
                comp.capitalize(),
                f"{subset['time_ms'].mean():.1f}",
                f"{subset['time_ms'].std():.1f}",
                f"{subset['time_ms'].median():.1f}",
                f"{subset['size_bytes'].mean():.0f}",
                f"{subset['size_bytes'].std():.0f}",
                f"{subset['size_bytes'].median():.0f}"
            ])
    
    columns = ['API', 'Complexidade', 
               'Tempo μ (ms)', 'Tempo σ', 'Tempo Med',
               'Tam. μ (B)', 'Tam. σ', 'Tam. Med']
    
    table = ax.table(cellText=summary_data, colLabels=columns,
                     loc='center', cellLoc='center',
                     colColours=['#4a90d9'] * 8)
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)
    
    # Estilizar cabeçalho
    for i in range(len(columns)):
        table[(0, i)].set_text_props(color='white', fontweight='bold')
    
    # Colorir linhas alternadas
    for i in range(len(summary_data)):
        for j in range(len(columns)):
            if i % 2 == 0:
                table[(i + 1, j)].set_facecolor('#e8f4f8')
            else:
                table[(i + 1, j)].set_facecolor('#ffffff')
    
    plt.title('Tabela Resumo: Estatísticas Descritivas', fontsize=16, fontweight='bold', pad=20)
    filepath = os.path.join(OUTPUT_DIR, '08_tabela_resumo.png')
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Salvo: {filepath}")

# ============================================
# GERAR DASHBOARD COMPLETO
# ============================================

def generate_dashboard(df):
    """Gera todos os gráficos do dashboard"""
    print("=" * 60)
    print("GERANDO DASHBOARD DE VISUALIZAÇÃO")
    print("=" * 60 + "\n")
    
    plot_time_boxplot(df)
    plot_size_boxplot(df)
    plot_distributions(df)
    plot_bar_ci(df)
    plot_violin(df)
    plot_heatmap(df)
    plot_summary(df)
    create_summary_table(df)
    
    print("\n" + "=" * 60)
    print("DASHBOARD GERADO COM SUCESSO!")
    print("=" * 60)
    print(f"\nArquivos salvos em: {OUTPUT_DIR}/")
    print("  - 01_tempo_boxplot.png")
    print("  - 02_tamanho_boxplot.png")
    print("  - 03_distribuicoes.png")
    print("  - 04_barras_ic95.png")
    print("  - 05_violin.png")
    print("  - 06_heatmap.png")
    print("  - 07_resumo_comparativo.png")
    print("  - 08_tabela_resumo.png")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("DASHBOARD: GraphQL vs REST")
    print("Laboratório de Experimentação de Software")
    print("=" * 60 + "\n")
    
    setup_output_dir()
    df = load_data()
    generate_dashboard(df)