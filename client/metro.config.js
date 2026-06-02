// client/metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Добавляем внешние папки для отслеживания
config.watchFolders = [
  __dirname,  // папка клиента
  'D:\\Documents\\main\\minecraft_all_textures'  // внешняя папка с текстурами
];

// Настраиваем resolver для работы с внешними ресурсами
config.resolver.assetExts.push('png', 'jpg', 'jpeg');
config.resolver.nodeModulesPaths = [
  __dirname + '/node_modules',
  'D:\\Documents\\main\\minecraft_all_textures'
];

module.exports = config;