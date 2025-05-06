
drop table if exists Usuario cascade;

create table Usuario (
    codUsuarioCPF    char(11) not null,
    nomUsuario       varchar(50) not null,
    desSenha         varchar(80),
    desEmail         varchar(50) not null,
    idtAdministrador boolean not null,
    idtFuncionario   boolean not null,
    idtGestor        boolean not null,
    idtAtivo         boolean not null,
    primary key (codUsuarioCPF)
);
