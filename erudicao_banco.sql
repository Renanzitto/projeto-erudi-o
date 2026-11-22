CREATE DATABASE IF NOT EXISTS Erudicao
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE Erudicao;

CREATE TABLE USUARIO (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  senha_hash VARCHAR(255) NOT NULL,
  perfil ENUM('colaborador', 'administrador') NOT NULL DEFAULT 'colaborador',
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE TEMA (
  id_tema INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL UNIQUE,
  descricao TEXT,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE REPERTORIO (
  id_repertorio INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  descricao TEXT NOT NULL,
  como_usar TEXT,
  fonte VARCHAR(255),
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  id_usuario_criador INT NOT NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_usuario_criador) REFERENCES USUARIO(id_usuario)
);
CREATE TABLE TEMA_REPERTORIO (
  id_tema INT NOT NULL,
  id_repertorio INT NOT NULL,
  PRIMARY KEY (id_tema, id_repertorio),
  FOREIGN KEY (id_tema) REFERENCES TEMA(id_tema) ON DELETE CASCADE,
  FOREIGN KEY (id_repertorio) REFERENCES REPERTORIO(id_repertorio) ON DELETE CASCADE
);
CREATE TABLE CONTRIBUICAO (
  id_contribuicao INT AUTO_INCREMENT PRIMARY KEY,
  id_tema INT NOT NULL,
  id_usuario INT NOT NULL,
  titulo VARCHAR(200) NOT NULL,
  descricao TEXT NOT NULL,
  como_usar TEXT,
  fonte VARCHAR(255),
  status ENUM('pendente', 'aprovada', 'rejeitada') NOT NULL DEFAULT 'pendente',
  id_admin_avaliador INT,
  avaliado_em DATETIME,
  id_repertorio INT,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_tema) REFERENCES TEMA(id_tema),
  FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario),
  FOREIGN KEY (id_admin_avaliador) REFERENCES USUARIO(id_usuario),
  FOREIGN KEY (id_repertorio) REFERENCES REPERTORIO(id_repertorio)
);