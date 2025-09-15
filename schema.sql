create table ativos
(
  id serial primary key,
  codigo varchar(12) not null unique,
  nome varchar(120),
  tipo varchar(20),
  setor varchar(80)
);

create table cotacoes
(
  id bigserial primary key,
  id_ativo int not null references ativos(id),
  data date not null,
  preco_abertura numeric(18,4),
  preco_fechamento numeric(18,4),
  maximo numeric(18,4),
  minimo numeric(18,4),
  negocios int,
  volume_financeiro numeric(20,2),
  unique (id_ativo, data)
);

create table dividendos
(
  id bigserial primary key,
  id_ativo int not null references ativos(id),
  data date not null,
  valor numeric(18,4) not null,
  tipo varchar(20),
  unique (id_ativo, data)
);

