"""
Análise Estatística: GraphQL vs REST
Disciplina: Laboratório de Experimentação de Software
Curso: Engenharia de Software
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Configuração
INPUT_DIR = "results"
INPUT_FILE = "experiment_results.csv"

# ============================================
# CARREGAR DADOS
# ============================================

def load_data():
    """Carrega os dados do experimento"""
    filepath = os.path.join(INPUT_DIR, INPUT_FILE)
    
    if not os.path.exists(filepath):
        print(f"ERRO: Arquivo não encontrado: {filepath}")
        print("Execute primeiro o experimento.py")
        exit(1)
    
    df = pd.read_csv(filepath)
    print(f"Dados carregados: {len(df)} registros")
    print(f"Colunas: {list(df.columns)}")
    print(f"APIs: {df['api_type'].unique()}")
    print(f"Complexidades: {df['complexity'].unique()}")
    print(f"Repositórios: {df['repository'].nunique()}\n")
    return df

# ============================================
# ESTATÍSTICAS DESCRITIVAS
# ============================================

def descriptive_stats(df):
    """Calcula e exibe estatísticas descritivas"""
    print("=" * 70)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("=" * 70)
    
    # Por tipo de API
    print("\n" + "-" * 70)
    print("TEMPO DE RESPOSTA (ms) - Por Tipo de API")
    print("-" * 70)
    time_stats = df.groupby('api_type')['time_ms'].agg([
        ('N', 'count'),
        ('Média', 'mean'),
        ('Desvio Padrão', 'std'),
        ('Mínimo', 'min'),
        ('Mediana', 'median'),
        ('Máximo', 'max')
    ]).round(2)
    print(time_stats.to_string())
    
    print("\n" + "-" * 70)
    print("TAMANHO DA RESPOSTA (bytes) - Por Tipo de API")
    print("-" * 70)
    size_stats = df.groupby('api_type')['size_bytes'].agg([
        ('N', 'count'),
        ('Média', 'mean'),
        ('Desvio Padrão', 'std'),
        ('Mínimo', 'min'),
        ('Mediana', 'median'),
        ('Máximo', 'max')
    ]).round(2)
    print(size_stats.to_string())
    
    # Por complexidade e API
    print("\n" + "-" * 70)
    print("TEMPO DE RESPOSTA (ms) - Por Complexidade e API")
    print("-" * 70)
    time_complex = df.groupby(['complexity', 'api_type'])['time_ms'].agg([
        ('N', 'count'),
        ('Média', 'mean'),
        ('Desvio Padrão', 'std'),
        ('Mediana', 'median')
    ]).round(2)
    print(time_complex.to_string())
    
    print("\n" + "-" * 70)
    print("TAMANHO DA RESPOSTA (bytes) - Por Complexidade e API")
    print("-" * 70)
    size_complex = df.groupby(['complexity', 'api_type'])['size_bytes'].agg([
        ('N', 'count'),
        ('Média', 'mean'),
        ('Desvio Padrão', 'std'),
        ('Mediana', 'median')
    ]).round(2)
    print(size_complex.to_string())
    
    return time_stats, size_stats

# ============================================
# TESTES DE NORMALIDADE
# ============================================

def normality_tests(df):
    """Executa testes de normalidade (Shapiro-Wilk)"""
    print("\n" + "=" * 70)
    print("TESTES DE NORMALIDADE (Shapiro-Wilk)")
    print("=" * 70)
    print("H0: Os dados seguem distribuição normal")
    print("H1: Os dados NÃO seguem distribuição normal")
    print("Nível de significância: α = 0.05")
    print("-" * 70)
    
    results = {}
    
    for api in ['REST', 'GraphQL']:
        for metric in ['time_ms', 'size_bytes']:
            data = df[df['api_type'] == api][metric]
            
            # Shapiro-Wilk (limitado a 5000 amostras)
            sample = data.sample(min(5000, len(data)), random_state=42)
            stat, p = stats.shapiro(sample)
            
            is_normal = "Sim" if p > 0.05 else "Não"
            decision = "Não rejeitar H0" if p > 0.05 else "Rejeitar H0"
            
            results[f"{api}_{metric}"] = {
                "statistic": stat,
                "p_value": p,
                "normal": is_normal
            }
            
            metric_name = "Tempo" if metric == "time_ms" else "Tamanho"
            print(f"{api:8} | {metric_name:8} | W = {stat:.4f} | p = {p:.6f} | Normal: {is_normal:3} | {decision}")
    
    print("-" * 70)
    print("Interpretação: Se p < 0.05, os dados NÃO são normais.")
    print("Recomendação: Usar testes não-paramétricos (Mann-Whitney U) se não normal.")
    
    return results

# ============================================
# TESTES DE HIPÓTESES
# ============================================

def hypothesis_tests(df):
    """Executa testes de hipóteses para RQ1 e RQ2"""
    print("\n" + "=" * 70)
    print("TESTES DE HIPÓTESES")
    print("=" * 70)
    
    # Separar dados
    rest_time = df[df['api_type'] == 'REST']['time_ms']
    graphql_time = df[df['api_type'] == 'GraphQL']['time_ms']
    rest_size = df[df['api_type'] == 'REST']['size_bytes']
    graphql_size = df[df['api_type'] == 'GraphQL']['size_bytes']
    
    results = {}
    
    # ==========================================
    # RQ1: TEMPO DE RESPOSTA
    # ==========================================
    print("\n" + "-" * 70)
    print("RQ1: Respostas GraphQL são mais rápidas que REST?")
    print("-" * 70)
    print("H0: μ_GraphQL = μ_REST (não há diferença significativa)")
    print("H1: μ_GraphQL ≠ μ_REST (há diferença significativa)")
    print("Nível de significância: α = 0.05")
    print()
    
    # Teste t (paramétrico)
    t_stat, t_p = stats.ttest_ind(rest_time, graphql_time)
    print(f"Teste t independente:")
    print(f"  t-statistic = {t_stat:.4f}")
    print(f"  p-value = {t_p:.6f}")
    
    # Mann-Whitney U (não paramétrico)
    u_stat, u_p = stats.mannwhitneyu(rest_time, graphql_time, alternative='two-sided')
    print(f"\nTeste Mann-Whitney U (não-paramétrico):")
    print(f"  U-statistic = {u_stat:.2f}")
    print(f"  p-value = {u_p:.6f}")
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((rest_time.std()**2 + graphql_time.std()**2) / 2)
    cohens_d_time = (rest_time.mean() - graphql_time.mean()) / pooled_std
    print(f"\nTamanho do efeito (Cohen's d): {cohens_d_time:.4f}")
    
    # Diferença percentual
    diff_pct = ((rest_time.mean() - graphql_time.mean()) / rest_time.mean()) * 100
    
    # Conclusão RQ1
    print(f"\n{'='*50}")
    if t_p < 0.05:
        if rest_time.mean() > graphql_time.mean():
            conclusion_rq1 = "GraphQL é significativamente MAIS RÁPIDO que REST"
        else:
            conclusion_rq1 = "REST é significativamente MAIS RÁPIDO que GraphQL"
        print(f"CONCLUSÃO RQ1: REJEITAR H0")
    else:
        conclusion_rq1 = "Não há diferença significativa no tempo de resposta"
        print(f"CONCLUSÃO RQ1: NÃO REJEITAR H0")
    
    print(f"{conclusion_rq1}")
    print(f"{'='*50}")
    print(f"Média REST: {rest_time.mean():.2f} ms")
    print(f"Média GraphQL: {graphql_time.mean():.2f} ms")
    print(f"Diferença: {diff_pct:+.2f}%")
    
    results['RQ1'] = {
        't_statistic': t_stat,
        't_p_value': t_p,
        'u_statistic': u_stat,
        'u_p_value': u_p,
        'cohens_d': cohens_d_time,
        'mean_rest': rest_time.mean(),
        'mean_graphql': graphql_time.mean(),
        'diff_percent': diff_pct,
        'conclusion': conclusion_rq1
    }
    
    # ==========================================
    # RQ2: TAMANHO DA RESPOSTA
    # ==========================================
    print("\n" + "-" * 70)
    print("RQ2: Respostas GraphQL têm tamanho menor que REST?")
    print("-" * 70)
    print("H0: μ_GraphQL = μ_REST (não há diferença significativa)")
    print("H1: μ_GraphQL ≠ μ_REST (há diferença significativa)")
    print("Nível de significância: α = 0.05")
    print()
    
    # Teste t (paramétrico)
    t_stat2, t_p2 = stats.ttest_ind(rest_size, graphql_size)
    print(f"Teste t independente:")
    print(f"  t-statistic = {t_stat2:.4f}")
    print(f"  p-value = {t_p2:.6f}")
    
    # Mann-Whitney U (não paramétrico)
    u_stat2, u_p2 = stats.mannwhitneyu(rest_size, graphql_size, alternative='two-sided')
    print(f"\nTeste Mann-Whitney U (não-paramétrico):")
    print(f"  U-statistic = {u_stat2:.2f}")
    print(f"  p-value = {u_p2:.6f}")
    
    # Effect size (Cohen's d)
    pooled_std2 = np.sqrt((rest_size.std()**2 + graphql_size.std()**2) / 2)
    cohens_d_size = (rest_size.mean() - graphql_size.mean()) / pooled_std2
    print(f"\nTamanho do efeito (Cohen's d): {cohens_d_size:.4f}")
    
    # Diferença percentual
    diff_pct2 = ((rest_size.mean() - graphql_size.mean()) / rest_size.mean()) * 100
    
    # Conclusão RQ2
    print(f"\n{'='*50}")
    if t_p2 < 0.05:
        if rest_size.mean() > graphql_size.mean():
            conclusion_rq2 = "GraphQL retorna respostas significativamente MENORES que REST"
        else:
            conclusion_rq2 = "REST retorna respostas significativamente MENORES que GraphQL"
        print(f"CONCLUSÃO RQ2: REJEITAR H0")
    else:
        conclusion_rq2 = "Não há diferença significativa no tamanho das respostas"
        print(f"CONCLUSÃO RQ2: NÃO REJEITAR H0")
    
    print(f"{conclusion_rq2}")
    print(f"{'='*50}")
    print(f"Média REST: {rest_size.mean():.0f} bytes")
    print(f"Média GraphQL: {graphql_size.mean():.0f} bytes")
    print(f"Diferença: {diff_pct2:+.2f}%")
    
    results['RQ2'] = {
        't_statistic': t_stat2,
        't_p_value': t_p2,
        'u_statistic': u_stat2,
        'u_p_value': u_p2,
        'cohens_d': cohens_d_size,
        'mean_rest': rest_size.mean(),
        'mean_graphql': graphql_size.mean(),
        'diff_percent': diff_pct2,
        'conclusion': conclusion_rq2
    }
    
    return results

# ============================================
# ANÁLISE POR COMPLEXIDADE
# ============================================

def analysis_by_complexity(df):
    """Análise detalhada por nível de complexidade"""
    print("\n" + "=" * 70)
    print("ANÁLISE POR NÍVEL DE COMPLEXIDADE")
    print("=" * 70)
    
    for complexity in ['simple', 'medium', 'complex']:
        subset = df[df['complexity'] == complexity]
        rest = subset[subset['api_type'] == 'REST']
        graphql = subset[subset['api_type'] == 'GraphQL']
        
        print(f"\n{'-'*70}")
        print(f"COMPLEXIDADE: {complexity.upper()}")
        print(f"{'-'*70}")
        
        # Tempo
        t_stat, t_p = stats.ttest_ind(rest['time_ms'], graphql['time_ms'])
        diff_time = ((rest['time_ms'].mean() - graphql['time_ms'].mean()) / rest['time_ms'].mean()) * 100
        sig_time = "***" if t_p < 0.001 else "**" if t_p < 0.01 else "*" if t_p < 0.05 else ""
        
        print(f"TEMPO DE RESPOSTA:")
        print(f"  REST:    {rest['time_ms'].mean():>10.2f} ms (±{rest['time_ms'].std():.2f})")
        print(f"  GraphQL: {graphql['time_ms'].mean():>10.2f} ms (±{graphql['time_ms'].std():.2f})")
        print(f"  Diferença: {diff_time:+.1f}% | p-value: {t_p:.6f} {sig_time}")
        
        # Tamanho
        t_stat2, t_p2 = stats.ttest_ind(rest['size_bytes'], graphql['size_bytes'])
        diff_size = ((rest['size_bytes'].mean() - graphql['size_bytes'].mean()) / rest['size_bytes'].mean()) * 100
        sig_size = "***" if t_p2 < 0.001 else "**" if t_p2 < 0.01 else "*" if t_p2 < 0.05 else ""
        
        print(f"\nTAMANHO DA RESPOSTA:")
        print(f"  REST:    {rest['size_bytes'].mean():>10.0f} bytes (±{rest['size_bytes'].std():.0f})")
        print(f"  GraphQL: {graphql['size_bytes'].mean():>10.0f} bytes (±{graphql['size_bytes'].std():.0f})")
        print(f"  Diferença: {diff_size:+.1f}% | p-value: {t_p2:.6f} {sig_size}")
    
    print(f"\n{'-'*70}")
    print("Legenda: * p<0.05 | ** p<0.01 | *** p<0.001")

# ============================================
# SUMÁRIO FINAL
# ============================================

def print_summary(results):
    """Imprime sumário final formatado"""
    print("\n" + "=" * 70)
    print("SUMÁRIO FINAL DO EXPERIMENTO")
    print("=" * 70)
    
    print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│ RQ1: Respostas GraphQL são mais rápidas que REST?                   │
├─────────────────────────────────────────────────────────────────────┤
│ Resultado: {results['RQ1']['conclusion']:<55} │
│ p-value: {results['RQ1']['t_p_value']:<59.6f} │
│ Cohen's d: {results['RQ1']['cohens_d']:<57.4f} │
│ Média REST: {results['RQ1']['mean_rest']:<51.2f} ms │
│ Média GraphQL: {results['RQ1']['mean_graphql']:<48.2f} ms │
│ Diferença: {results['RQ1']['diff_percent']:+<56.2f}% │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ RQ2: Respostas GraphQL têm tamanho menor que REST?                  │
├─────────────────────────────────────────────────────────────────────┤
│ Resultado: {results['RQ2']['conclusion']:<55} │
│ p-value: {results['RQ2']['t_p_value']:<59.6f} │
│ Cohen's d: {results['RQ2']['cohens_d']:<57.4f} │
│ Média REST: {results['RQ2']['mean_rest']:<48.0f} bytes │
│ Média GraphQL: {results['RQ2']['mean_graphql']:<45.0f} bytes │
│ Diferença: {results['RQ2']['diff_percent']:+<56.2f}% │
└─────────────────────────────────────────────────────────────────────┘

Interpretação do Cohen's d:
  |d| < 0.2  : Efeito desprezível
  0.2 ≤ |d| < 0.5 : Efeito pequeno
  0.5 ≤ |d| < 0.8 : Efeito médio
  |d| ≥ 0.8  : Efeito grande
""")

# ============================================
# EXPORTAR RESULTADOS
# ============================================

def export_analysis_results(results, df):
    """Exporta resultados da análise para CSV"""
    # Criar DataFrame com resultados dos testes
    analysis_data = []
    
    for rq, data in results.items():
        analysis_data.append({
            'research_question': rq,
            'metric': 'time_ms' if rq == 'RQ1' else 'size_bytes',
            't_statistic': data['t_statistic'],
            't_p_value': data['t_p_value'],
            'u_statistic': data['u_statistic'],
            'u_p_value': data['u_p_value'],
            'cohens_d': data['cohens_d'],
            'mean_rest': data['mean_rest'],
            'mean_graphql': data['mean_graphql'],
            'diff_percent': data['diff_percent'],
            'conclusion': data['conclusion'],
            'significant': data['t_p_value'] < 0.05
        })
    
    analysis_df = pd.DataFrame(analysis_data)
    filepath = os.path.join(INPUT_DIR, 'analysis_results.csv')
    analysis_df.to_csv(filepath, index=False)
    print(f"\nResultados da análise exportados para: {filepath}")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 70)
    print("ANÁLISE ESTATÍSTICA: GraphQL vs REST")
    print("Laboratório de Experimentação de Software")
    print("=" * 70 + "\n")
    
    # Carregar dados
    df = load_data()
    
    # Estatísticas descritivas
    descriptive_stats(df)
    
    # Testes de normalidade
    normality_tests(df)
    
    # Testes de hipóteses
    results = hypothesis_tests(df)
    
    # Análise por complexidade
    analysis_by_complexity(df)
    
    # Sumário final
    print_summary(results)
    
    # Exportar resultados
    export_analysis_results(results, df)
    
    print("\n" + "=" * 70)
    print("ANÁLISE CONCLUÍDA!")
    print("=" * 70)