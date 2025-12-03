"""
Experimento Controlado: GraphQL vs REST
Disciplina: Laboratório de Experimentação de Software
Curso: Engenharia de Software
"""

import requests
import time
import json
import csv
import random
import os
from datetime import datetime


# Gere seu token em: https://github.com/settings/tokens
GITHUB_TOKEN = "TOKEN"

# Headers para as requisições
HEADERS_REST = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Cache-Control": "no-cache"
}

HEADERS_GRAPHQL = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache"
}

# URLs das APIs
REST_URL = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"

# Repositórios para teste (owner/repo)
REPOS = [
    ("facebook", "react"),
    ("microsoft", "vscode"),
    ("tensorflow", "tensorflow"),
    ("torvalds", "linux"),
    ("django", "django"),
    ("python", "cpython"),
    ("nodejs", "node"),
    ("kubernetes", "kubernetes"),
    ("angular", "angular"),
    ("vuejs", "vue")
]

# Configurações do experimento
NUM_EXECUTIONS = 100  # Número de repetições por tratamento
WARMUP_RUNS = 5       # Requisições de aquecimento (descartadas)
OUTPUT_DIR = "results"  # Pasta para salvar resultados

# ============================================
# FUNÇÕES DE CONSULTA REST
# ============================================

def rest_simple(owner, repo):
    """Consulta simples: dados básicos do repositório"""
    url = f"{REST_URL}/repos/{owner}/{repo}"
    start = time.perf_counter()
    response = requests.get(url, headers=HEADERS_REST)
    end = time.perf_counter()
    return {
        "time_ms": (end - start) * 1000,
        "size_bytes": len(response.content),
        "status": response.status_code
    }

def rest_medium(owner, repo):
    """Consulta média: repositório + últimos 10 issues"""
    url_repo = f"{REST_URL}/repos/{owner}/{repo}"
    url_issues = f"{REST_URL}/repos/{owner}/{repo}/issues?per_page=10&state=all"
    
    start = time.perf_counter()
    r1 = requests.get(url_repo, headers=HEADERS_REST)
    r2 = requests.get(url_issues, headers=HEADERS_REST)
    end = time.perf_counter()
    
    return {
        "time_ms": (end - start) * 1000,
        "size_bytes": len(r1.content) + len(r2.content),
        "status": r1.status_code
    }

def rest_complex(owner, repo):
    """Consulta complexa: repo + issues + contributors + branches"""
    urls = [
        f"{REST_URL}/repos/{owner}/{repo}",
        f"{REST_URL}/repos/{owner}/{repo}/issues?per_page=5&state=all",
        f"{REST_URL}/repos/{owner}/{repo}/contributors?per_page=5",
        f"{REST_URL}/repos/{owner}/{repo}/branches?per_page=5"
    ]
    
    start = time.perf_counter()
    responses = [requests.get(url, headers=HEADERS_REST) for url in urls]
    end = time.perf_counter()
    
    total_size = sum(len(r.content) for r in responses)
    return {
        "time_ms": (end - start) * 1000,
        "size_bytes": total_size,
        "status": responses[0].status_code
    }

# ============================================
# FUNÇÕES DE CONSULTA GRAPHQL
# ============================================

def graphql_simple(owner, repo):
    """Consulta simples: dados básicos do repositório"""
    query = """
    query($owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
            name
            description
            stargazerCount
            forkCount
            createdAt
            updatedAt
            primaryLanguage { name }
        }
    }
    """
    variables = {"owner": owner, "repo": repo}
    
    start = time.perf_counter()
    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS_GRAPHQL,
        json={"query": query, "variables": variables}
    )
    end = time.perf_counter()
    
    return {
        "time_ms": (end - start) * 1000,
        "size_bytes": len(response.content),
        "status": response.status_code
    }

def graphql_medium(owner, repo):
    """Consulta média: repositório + últimos 10 issues"""
    query = """
    query($owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
            name
            description
            stargazerCount
            forkCount
            issues(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                    title
                    state
                    createdAt
                    author { login }
                }
            }
        }
    }
    """
    variables = {"owner": owner, "repo": repo}
    
    start = time.perf_counter()
    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS_GRAPHQL,
        json={"query": query, "variables": variables}
    )
    end = time.perf_counter()
    
    return {
        "time_ms": (end - start) * 1000,
        "size_bytes": len(response.content),
        "status": response.status_code
    }

def graphql_complex(owner, repo):
    """Consulta complexa: repo + issues + contributors + branches"""
    query = """
    query($owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
            name
            description
            stargazerCount
            forkCount
            issues(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes { title state createdAt }
            }
            mentionableUsers(first: 5) {
                nodes { login name }
            }
            refs(refPrefix: "refs/heads/", first: 5) {
                nodes { name }
            }
        }
    }
    """
    variables = {"owner": owner, "repo": repo}
    
    start = time.perf_counter()
    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS_GRAPHQL,
        json={"query": query, "variables": variables}
    )
    end = time.perf_counter()
    
    return {
        "time_ms": (end - start) * 1000,
        "size_bytes": len(response.content),
        "status": response.status_code
    }

# ============================================
# EXECUÇÃO DO EXPERIMENTO
# ============================================

def run_warmup():
    """Executa requisições de aquecimento"""
    print("Executando warm-up...")
    for _ in range(WARMUP_RUNS):
        rest_simple("octocat", "Hello-World")
        graphql_simple("octocat", "Hello-World")
    print("Warm-up concluído!\n")

def run_experiment():
    """Executa o experimento completo"""
    results = []
    
    # Tratamentos
    treatments = [
        ("REST", "simple", rest_simple),
        ("GraphQL", "simple", graphql_simple),
        ("REST", "medium", rest_medium),
        ("GraphQL", "medium", graphql_medium),
        ("REST", "complex", rest_complex),
        ("GraphQL", "complex", graphql_complex)
    ]
    
    total = len(treatments) * len(REPOS) * NUM_EXECUTIONS
    current = 0
    
    print(f"Iniciando experimento: {total} medições no total\n")
    
    # Aleatorizar ordem para reduzir viés
    experiment_runs = []
    for api_type, complexity, func in treatments:
        for owner, repo in REPOS:
            for run in range(NUM_EXECUTIONS):
                experiment_runs.append((api_type, complexity, func, owner, repo, run))
    
    random.shuffle(experiment_runs)
    
    for api_type, complexity, func, owner, repo, run in experiment_runs:
        current += 1
        try:
            result = func(owner, repo)
            results.append({
                "timestamp": datetime.now().isoformat(),
                "api_type": api_type,
                "complexity": complexity,
                "repository": f"{owner}/{repo}",
                "execution": run + 1,
                "time_ms": round(result["time_ms"], 2),
                "size_bytes": result["size_bytes"],
                "status": result["status"]
            })
            
            if current % 100 == 0:
                print(f"Progresso: {current}/{total} ({100*current/total:.1f}%)")
                
        except Exception as e:
            print(f"Erro em {api_type} {complexity} {owner}/{repo}: {e}")
            
        # Pequena pausa para evitar rate limiting
        time.sleep(0.1)
    
    return results

# ============================================
# SALVAR RESULTADOS
# ============================================

def save_results(results, filename="experiment_results.csv"):
    """Salva resultados em CSV"""
    if not results:
        print("Nenhum resultado para salvar!")
        return
    
    # Criar pasta de resultados se não existir
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    keys = results[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nResultados salvos em: {filepath}")
    
    # Salvar também resumos estatísticos
    save_summary(results)

def save_summary(results):
    """Salva resumos estatísticos em CSVs separados"""
    import pandas as pd
    df = pd.DataFrame(results)
    
    # Resumo geral por API
    summary_api = df.groupby('api_type').agg({
        'time_ms': ['count', 'mean', 'std', 'min', 'median', 'max'],
        'size_bytes': ['mean', 'std', 'min', 'median', 'max']
    }).round(2)
    summary_api.to_csv(os.path.join(OUTPUT_DIR, 'summary_by_api.csv'))
    
    # Resumo por API e complexidade
    summary_detail = df.groupby(['api_type', 'complexity']).agg({
        'time_ms': ['count', 'mean', 'std', 'min', 'median', 'max'],
        'size_bytes': ['mean', 'std', 'min', 'median', 'max']
    }).round(2)
    summary_detail.to_csv(os.path.join(OUTPUT_DIR, 'summary_by_complexity.csv'))
    
    # Resumo por repositório
    summary_repo = df.groupby(['repository', 'api_type', 'complexity']).agg({
        'time_ms': ['mean', 'std'],
        'size_bytes': ['mean', 'std']
    }).round(2)
    summary_repo.to_csv(os.path.join(OUTPUT_DIR, 'summary_by_repository.csv'))
    
    print("\nResumos estatísticos salvos em:")
    print(f"  - {OUTPUT_DIR}/summary_by_api.csv")
    print(f"  - {OUTPUT_DIR}/summary_by_complexity.csv")
    print(f"  - {OUTPUT_DIR}/summary_by_repository.csv")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENTO CONTROLADO: GraphQL vs REST")
    print("Laboratório de Experimentação de Software")
    print("=" * 60)
    print(f"Data/Hora de Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repositórios: {len(REPOS)}")
    print(f"Execuções por tratamento: {NUM_EXECUTIONS}")
    print(f"Total de medições: {len(REPOS) * NUM_EXECUTIONS * 6}")
    print("=" * 60 + "\n")
    
    # Verificar token
    if GITHUB_TOKEN == "SEU_TOKEN_AQUI":
        print("=" * 60)
        print("ERRO: Configure seu token do GitHub!")
        print("=" * 60)
        print("\n1. Acesse: https://github.com/settings/tokens")
        print("2. Clique em 'Generate new token (classic)'")
        print("3. Marque as permissões: 'repo' e 'read:user'")
        print("4. Copie o token e cole na variável GITHUB_TOKEN")
        print("\nExemplo:")
        print('GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"')
        exit(1)
    
    # Testar conexão
    print("Testando conexão com GitHub API...")
    try:
        test = requests.get(f"{REST_URL}/user", headers=HEADERS_REST)
        if test.status_code == 200:
            print(f"Conectado como: {test.json().get('login', 'N/A')}\n")
        else:
            print(f"Erro de autenticação: {test.status_code}")
            exit(1)
    except Exception as e:
        print(f"Erro de conexão: {e}")
        exit(1)
    
    # Executar experimento
    run_warmup()
    results = run_experiment()
    save_results(results)
    
    print("\n" + "=" * 60)
    print("EXPERIMENTO CONCLUÍDO COM SUCESSO!")
    print(f"Data/Hora de Término: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"\nPróximos passos:")
    print(f"1. Execute 'python analise.py' para análise estatística")
    print(f"2. Execute 'python dashboard.py' para gerar gráficos")