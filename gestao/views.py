# -*- coding: utf-8 -*-
#
#  Copyleft (c) 2011 André Filipe A. Brito e contribuidores
#
#
#  Conselhos is free software under terms of the GNU Affero General Public
#  License version 3 (AGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.db.models import Q
from gestao.models import Conselho, Legislacao, Mandato, EstruturaRegimental, CargoRegimental, Conselheiro


def index(request):
    conselhos = Conselho.objects.all()
    return render_to_response('gestao/conselhos.html', {'conselhos': conselhos})


def conselhos(request, categoria):
    conselhos = get_list_or_404(Conselho, categoria=categoria)
    descricao = conselhos[0].get_categoria_display()
    return render_to_response('gestao/conselhos_categ.html', {'conselhos': conselhos, 'descricao': descricao})


def conselho(request, conselho_id):
    conselho = get_object_or_404(Conselho, pk=conselho_id)
    legislacoes = Legislacao.objects.filter(conselho=conselho)  # Retorna todas as legislações do conselho
    fundacao = legislacoes.order_by('data')[0]  # Retorna a legislação mais antiga como a que funda o conselho
    mandatos = conselho.mandato()  # Recupera os mandatos
    estrutura = EstruturaRegimental.objects.filter(conselho=conselho).latest('data')  # Recupera a ultima estrutura disponível pro conselho
    cargosregimentais = CargoRegimental.objects.filter(estrutura=estrutura)  # Recupera todos os cargos da ultima estrutura

    n_cargos = cargosregimentais.count()
    n_cargos_ocupados = mandatos.count()
    n_cargos_livres = n_cargos - n_cargos_ocupados

    n_cargos_previstos = cargosregimentais.exclude(legislacao__isnull=True).count()
    n_cargos_previstos_ocupados = mandatos.exclude(cargo__legislacao__isnull=True).count()
    n_cargos_previstos_livres = n_cargos_previstos - n_cargos_previstos_ocupados

    n_cargos_nprevistos = n_cargos - n_cargos_previstos
    n_cargos_nprevistos_ocupados = mandatos.exclude(cargo__legislacao__isnull=False).count()
    n_cargos_nprevistos_livres = n_cargos_nprevistos - n_cargos_nprevistos_ocupados

    # Estatisticas sobre o conselho
    poder_sociedade = cargosregimentais.filter(poder='SC')
    poder_pub_dist = cargosregimentais.filter(Q(poder='PED') | Q(poder='PLD') | Q(poder='PJD'))
    poder_pub_fed = cargosregimentais.filter(Q(poder='PEF') | Q(poder='PLF') | Q(poder='PJF'))

    # Membros Natos da Sociedade Civil
    cargo_membro_nato_sc = poder_sociedade.filter(cargo='MNSC')  # Filtra os cargos Membros Natos da Sociedade Civil
    cargo_membro_nato_pp_dist_sc = poder_pub_dist.filter(cargo='MNSC')  # Filtra os cargos Membros Natos da Sociedade Civil
    cargo_membro_nato_pp_fed_sc = poder_pub_fed.filter(cargo='MNSC')  # Filtra os cargos Membros Natos da Sociedade Civil

    # Membros Natos do Poder Público
    cargo_membro_nato_sc_pp = poder_sociedade.filter(cargo='MNPP')  # Filtra os cargos Membros Natos do Poder Público
    cargo_membro_nato_pp_dist = poder_pub_dist.filter(cargo='MNPP')  # Filtra os cargos Membros Natos do Poder Público
    cargo_membro_nato_pp_fed = poder_pub_fed.filter(cargo='MNPP')  # Filtra os cargos Membros Natos do Poder Público

    # Indicação Institucional da Sociedade Civil
    cargo_indicacao_sc = poder_sociedade.filter(cargo='IISC')  # Filtra os cargos de indicação Institucional da Sociedade Civil
    cargo_indicacao_sc_pp_dist = poder_pub_dist.filter(cargo='IISC')  # Filtra os cargos de indicação Institucional do Poder Público
    cargo_indicacao_sc_pp_fed = poder_pub_fed.filter(cargo='IISC')

    # Indicação Institucional da Sociedade Civil por Eleição
    cargo_indicacao_eleicao = poder_sociedade.filter(cargo='IISCE')  # Filtra os cargos de indicação Institucional da Sociedade Civil por Eleição
    cargo_indicacao_eleicao_pp_dist = poder_pub_dist.filter(cargo='IISCE')  # Filtra os cargos de indicação Institucional da Sociedade Civil por Eleição
    cargo_indicacao_eleicao_pp_fed = poder_pub_fed.filter(cargo='IISCE')  # Filtra os cargos de indicação Institucional da Sociedade Civil por Eleição

    # Indicação Institucional do Poder Público
    cargo_indicacao_pp_sc = poder_sociedade.filter(cargo='IIPP')
    cargo_indicacao_pp_dist = poder_pub_dist.filter(cargo='IIPP')
    cargo_indicacao_pp_fed = poder_pub_fed.filter(cargo='IIPP')

    # Indicação por Gestor da Área
    cargo_indicacao_sc_gestor = poder_sociedade.filter(cargo='IPGA')  # Filtra os cargos de indicação por Gestor da Área
    cargo_indicacao_pp_dist_gestor = poder_pub_dist.filter(cargo='IPGA')
    cargo_indicacao_pp_fed_gestor = poder_pub_fed.filter(cargo='IPGA')

    # Indicação por Gestor da Área por Lista Triplice
    cargo_indicacao_sc_gestorlt = poder_sociedade.filter(cargo='IPGAT')
    cargo_indicacao_pp_dist_gestorlt = poder_pub_dist.filter(cargo='IPGAT')
    cargo_indicacao_pp_fed_gestorlt = poder_pub_fed.filter(cargo='IPGAT')

    # Indicação pelo Governador
    cargo_indicacao_sc_gov = poder_sociedade.filter(cargo='IPG')  # Filtra os cargos de indicação pelo Governador
    cargo_indicacao_pp_dist_gov = poder_pub_dist.filter(cargo='IPG')  # Filtra os cargos de indicação pelo Governador
    cargo_indicacao_pp_fed_gov = poder_pub_fed.filter(cargo='IPG')  # Filtra os cargos de indicação pelo Governador

    # Indicação pelo Governador por Lista Triplice
    cargo_indicacao_sc_govlt = poder_sociedade.filter(cargo='IPGT')  # Filtra os cargos de indicação pelo Governador por Lista Triplice
    cargo_indicacao_pp_dist_govlt = poder_pub_dist.filter(cargo='IPGT')  # Filtra os cargos de indicação pelo Governador por Lista Triplice
    cargo_indicacao_pp_fed_govlt = poder_pub_fed.filter(cargo='IPGT')  # Filtra os cargos de indicação pelo Governador por Lista Triplice

    # Indicação pelo Segmento da Sociedade Cívil
    cargo_indicacao_sc_segsc = poder_sociedade.filter(cargo='IPS')  # Filtra os cargos de indicação pelo Segmento da Sociedade Cívil
    cargo_indicacao_pp_dist_segsc = poder_pub_dist.filter(cargo='IPS')  # Filtra os cargos de indicação pelo Segmento da Sociedade Cívil
    cargo_indicacao_pp_fed_segsc = poder_pub_fed.filter(cargo='IPS')  # Filtra os cargos de indicação pelo Segmento da Sociedade Cívil

    # Indicação pelo Segmento da Sociedade Civil por Eleição
    cargo_indicacao_sc_segsce = poder_sociedade.filter(cargo='IPSE')  # Filtra os cargos de indicação pelo Segmento da Sociedade Cívil por Eleição
    cargo_indicacao_pp_dist_segsce = poder_pub_dist.filter(cargo='IPSE')  # Filtra os cargos de indicação pelo Segmento da Sociedade Cívil por Eleição
    cargo_indicacao_pp_fed_segsce = poder_pub_fed.filter(cargo='IPSE')  # Filtra os cargos de indicação pelo Segmento da Sociedade Cívil por Eleição

    return render_to_response('gestao/conselho.html', {
        'conselho': conselho,
        'legislacoes': legislacoes,
        'fundacao': fundacao,
        'mandatos': mandatos,
        'cargosregimentais': cargosregimentais,
        'n_cargos': n_cargos,
        'n_cargos_ocupados': n_cargos_ocupados,
        'n_cargos_livres': n_cargos_livres,
        'n_cargos_previstos': n_cargos_previstos,
        'n_cargos_previstos_ocupados': n_cargos_previstos_ocupados,
        'n_cargos_previstos_livres': n_cargos_previstos_livres,
        'n_cargos_nprevistos': n_cargos_nprevistos,
        'n_cargos_nprevistos_ocupados': n_cargos_nprevistos_ocupados,
        'n_cargos_nprevistos_livres': n_cargos_nprevistos_livres,

        # Estatisticas
        'cargo_membro_nato_sc': cargo_membro_nato_sc,
        'cargo_membro_nato_pp_dist_sc': cargo_membro_nato_pp_dist_sc,
        'cargo_membro_nato_pp_fed_sc': cargo_membro_nato_pp_fed_sc,

        # Membros Natos do Poder Público
        'cargo_membro_nato_sc_pp': cargo_membro_nato_sc_pp,
        'cargo_membro_nato_pp_dist': cargo_membro_nato_pp_dist,
        'cargo_membro_nato_pp_fed': cargo_membro_nato_pp_fed,

        # Indicação Institucional da Sociedade Civil
        'cargo_indicacao_sc': cargo_indicacao_sc,
        'cargo_indicacao_sc_pp_dist': cargo_indicacao_sc_pp_dist,
        'cargo_indicacao_sc_pp_fed': cargo_indicacao_sc_pp_fed,

        # Indicação Institucional da Sociedade Civil por Eleição
        'cargo_indicacao_eleicao': cargo_indicacao_eleicao,
        'cargo_indicacao_eleicao_pp_dist': cargo_indicacao_eleicao_pp_dist,
        'cargo_indicacao_eleicao_pp_fed': cargo_indicacao_eleicao_pp_fed,

        # Indicação Institucional do Poder Público
        'cargo_indicacao_pp_sc': cargo_indicacao_pp_sc,
        'cargo_indicacao_pp_dist': cargo_indicacao_pp_dist,
        'cargo_indicacao_pp_fed': cargo_indicacao_pp_fed,

        # Indicação por Gestor da Área
        'cargo_indicacao_sc_gestor': cargo_indicacao_sc_gestor,
        'cargo_indicacao_pp_dist_gestor': cargo_indicacao_pp_dist_gestor,
        'cargo_indicacao_pp_fed_gestor': cargo_indicacao_pp_fed_gestor,

        # Indicação por Gestor da Área por Lista Triplice
        'cargo_indicacao_sc_gestorlt': cargo_indicacao_sc_gestorlt,
        'cargo_indicacao_pp_dist_gestorlt': cargo_indicacao_pp_dist_gestorlt,
        'cargo_indicacao_pp_fed_gestorlt': cargo_indicacao_pp_fed_gestorlt,

        # Indicação pelo Governador
        'cargo_indicacao_sc_gov': cargo_indicacao_sc_gov,
        'cargo_indicacao_pp_dist_gov': cargo_indicacao_pp_dist_gov,
        'cargo_indicacao_pp_fed_gov': cargo_indicacao_pp_fed_gov,

        # Indicação pelo Governador por Lista Triplice
        'cargo_indicacao_sc_govlt': cargo_indicacao_sc_govlt,
        'cargo_indicacao_pp_dist_govlt': cargo_indicacao_pp_dist_govlt,
        'cargo_indicacao_pp_fed_govlt': cargo_indicacao_pp_fed_govlt,

        # Indicação pelo Segmento da Sociedade Cívil
        'cargo_indicacao_sc_segsc': cargo_indicacao_sc_segsc,
        'cargo_indicacao_pp_dist_segsc': cargo_indicacao_pp_dist_segsc,
        'cargo_indicacao_pp_fed_segsc': cargo_indicacao_pp_fed_segsc,

        # Indicação pelo Segmento da Sociedade Civil por Eleição
        'cargo_indicacao_sc_segsce': cargo_indicacao_sc_segsce,
        'cargo_indicacao_pp_dist_segsce': cargo_indicacao_pp_dist_segsce,
        'cargo_indicacao_pp_fed_segsce': cargo_indicacao_pp_fed_segsce

        }
        )


def conselheiro(request, conselheiro_id):
    conselheiro = get_object_or_404(Conselheiro, pk=conselheiro_id)
    mandatos = Mandato.objects.filter(Q(titular=conselheiro_id) | Q(suplente=conselheiro_id)).order_by('-data_inicial', '-data_termino')
    return render_to_response('gestao/conselheiro.html', {'conselheiro': conselheiro, 'mandatos': mandatos})
