const { UserService } = require('../src/userService');

describe('UserService - comportamentos do gerenciamento de usuários', () => {
  let userService;

  beforeEach(() => {
    userService = new UserService();
    userService._clearDB();
  });

  describe('createUser', () => {
    test('cria um usuário ativo com os dados informados e um identificador', () => {
      // Arrange
      const dados = { nome: 'Alice', email: 'alice@email.com', idade: 28 };

      // Act
      const usuario = userService.createUser(dados.nome, dados.email, dados.idade);

      // Assert
      expect(usuario).toEqual(expect.objectContaining({
        ...dados,
        id: expect.stringMatching(/\S/),
        createdAt: expect.any(Date),
        status: 'ativo',
      }));
    });

    test('cria um usuário comum quando a permissão de administrador é omitida', () => {
      // Arrange
      const dados = { nome: 'Comum', email: 'comum@teste.com', idade: 30 };

      // Act
      const usuario = userService.createUser(dados.nome, dados.email, dados.idade);

      // Assert
      expect(usuario.isAdmin).toBe(false);
    });

    test('cria um administrador quando a permissão é solicitada', () => {
      // Arrange
      const dados = { nome: 'Admin', email: 'admin@teste.com', idade: 40 };

      // Act
      const usuario = userService.createUser(dados.nome, dados.email, dados.idade, true);

      // Assert
      expect(usuario.isAdmin).toBe(true);
    });

    test('aceita um usuário com exatamente 18 anos', () => {
      // Arrange
      const dados = { nome: 'Adulto', email: 'adulto@teste.com', idade: 18 };

      // Act
      const usuario = userService.createUser(dados.nome, dados.email, dados.idade);

      // Assert
      expect(usuario.idade).toBe(18);
    });

    test('rejeita um usuário menor de idade', () => {
      // Arrange
      const dados = { nome: 'Menor', email: 'menor@email.com', idade: 17 };

      // Act
      const criarMenor = () => userService.createUser(dados.nome, dados.email, dados.idade);

      // Assert
      expect(criarMenor).toThrow('O usuário deve ser maior de idade.');
    });

    test.each([
      ['nome', '', 'alice@email.com', 28],
      ['email', 'Alice', '', 28],
      ['idade', 'Alice', 'alice@email.com', undefined],
    ])('rejeita a criação quando %s está ausente', (_campo, nome, email, idade) => {
      // Arrange
      const dados = { nome, email, idade };

      // Act
      const criarSemCampo = () => userService.createUser(dados.nome, dados.email, dados.idade);

      // Assert
      expect(criarSemCampo).toThrow('Nome, email e idade são obrigatórios.');
    });

    test('atribui identificadores diferentes a usuários distintos', () => {
      // Arrange
      const primeiro = userService.createUser('Alice', 'alice@email.com', 28);

      // Act
      const segundo = userService.createUser('Bob', 'bob@email.com', 32);

      // Assert
      expect(segundo.id).not.toBe(primeiro.id);
    });
  });

  describe('getUserById', () => {
    test('recupera os dados de um usuário cadastrado pelo identificador retornado', () => {
      // Arrange
      const cadastrado = userService.createUser('Alice', 'alice@email.com', 28);

      // Act
      const encontrado = userService.getUserById(cadastrado.id);

      // Assert
      expect(encontrado).toEqual(expect.objectContaining({
        id: cadastrado.id,
        nome: 'Alice',
        email: 'alice@email.com',
        idade: 28,
        status: 'ativo',
      }));
    });

    test('retorna null para um identificador não cadastrado', () => {
      // Arrange
      const idInexistente = 'usuario-inexistente';

      // Act
      const usuario = userService.getUserById(idInexistente);

      // Assert
      expect(usuario).toBeNull();
    });
  });

  describe('deactivateUser', () => {
    test('desativa um usuário comum e preserva seu cadastro', () => {
      // Arrange
      const usuario = userService.createUser('Comum', 'comum@teste.com', 30);

      // Act
      const resultado = userService.deactivateUser(usuario.id);

      // Assert
      expect(resultado).toBe(true);
      expect(userService.getUserById(usuario.id)).toEqual(expect.objectContaining({
        id: usuario.id,
        nome: 'Comum',
        email: 'comum@teste.com',
        idade: 30,
        isAdmin: false,
        status: 'inativo',
      }));
    });

    test('recusa desativar um administrador e mantém seu status ativo', () => {
      // Arrange
      const admin = userService.createUser('Admin', 'admin@teste.com', 40, true);

      // Act
      const resultado = userService.deactivateUser(admin.id);

      // Assert
      expect(resultado).toBe(false);
      expect(userService.getUserById(admin.id)).toEqual(expect.objectContaining({
        id: admin.id,
        isAdmin: true,
        status: 'ativo',
      }));
    });

    test('retorna false ao tentar desativar um usuário inexistente', () => {
      // Arrange
      const idInexistente = 'usuario-inexistente';

      // Act
      const resultado = userService.deactivateUser(idInexistente);

      // Assert
      expect(resultado).toBe(false);
      expect(userService.getUserById(idInexistente)).toBeNull();
    });
  });

  describe('generateUserReport', () => {
    test('informa a ausência de usuários quando não há cadastros', () => {
      // Arrange
      // O beforeEach mantém o banco vazio para este cenário.

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain('Nenhum usuário cadastrado.');
    });

    test('inclui os identificadores e nomes de todos os usuários cadastrados', () => {
      // Arrange
      const alice = userService.createUser('Alice', 'alice@email.com', 28);
      const bob = userService.createUser('Bob', 'bob@email.com', 32);

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain(alice.id);
      expect(relatorio).toContain('Alice');
      expect(relatorio).toContain(bob.id);
      expect(relatorio).toContain('Bob');
    });

    test('informa o status ativo de um usuário recém-cadastrado', () => {
      // Arrange
      userService.createUser('Alice', 'alice@email.com', 28);

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain('ativo');
      expect(relatorio).not.toContain('inativo');
    });

    test('mantém o usuário desativado no relatório com o status inativo', () => {
      // Arrange
      const usuario = userService.createUser('Alice', 'alice@email.com', 28);
      userService.deactivateUser(usuario.id);

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain(usuario.id);
      expect(relatorio).toContain('Alice');
      expect(relatorio).toContain('inativo');
    });
  });
});
