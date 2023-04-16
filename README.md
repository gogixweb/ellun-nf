Gerador de link para preenchimento do formulário de solicitação de NF da Ellun Contabilidade.
Este pacote fornece um script `ellunf` que aceita um valor e utiliza um arquivo de configuração para gerar um link para
o formulário da Ellun já pré-preenchido.

Espero que seja proveitoso!

## Instalação

Crie um e ative um virtualenv Python:
```shell
python -m venv .venv
source .venv/bin/activate\n
```
Instale o pacote ellun-nf utilizando a URL do Github:
```shell
pip install git+http://github.com/gogixweb/ellun-nf.git@main
```

## Configuração
Crie um arquivo `.ini` como no exemplo abaixo:
```ini
[company]
name = Minha Empresa ME
tax = Simples

[client]
name = Cliente Internacional Inc
transfer_fee = 0.96

[services]
Instalação e implantação de aplicativos = 51
Manutenção e modificações em sistemas para atender a necessidades técnicas = 49
```

Caso você receba em dólares e utilize uma plataforma como a Remessa Online ou Husky, utilize a configuração
`transfer_fee` para a porcentagem/spread cobrados.

Caso sua empresa esteja enquadrada no lucro presumido, utilize `tax = LP`.

Você pode listar quantos serviços quiser em `[services]`, e os números representam as porcentagems que cada serviço
representará na nota fiscal.

## Utilização

```shell
ellunf valor_da_nf [valor_da_taxa_de_cambio]
```
O valor da taxa de câmbio é dado em porcentagem, e caso não seja fornecido é utilizado o valor contido no arquivo `.ini`.

Supondo que o seu arquivo `.ini` esteja salvo como `/path/to/ellunnf.ini`, você pode fazer:
```shell
export ELLUNNF_INI=/path/to/ellunnf.ini
ellunf 1000 0
```
Ou:
```shell
ELLUNNF_INI=/path/to/ellunnf.ini ellunf 1000 0
```

Saída:
```shell
# Minha Empresa ME
# Cliente Internacional Inc
# N/A
# MM/YYYY
# instalação e implantação de aplicativos - R$ 510,00, \
# manutenção e modificações em sistemas para atender a necessidades técnicas - R$ 490,00
# 1000.00
# https://docs.google.com/forms/d/1dBGSh... (link para o form preenchido)
```
