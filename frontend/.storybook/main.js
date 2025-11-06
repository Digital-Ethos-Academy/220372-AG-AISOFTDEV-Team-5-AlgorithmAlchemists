module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|mdx)'],
  addons: [
    '@storybook/preset-create-react-app',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions'
  ],
  framework: {
    name: '@storybook/react-webpack5',
    options: {}
  },
  docs: { autodocs: true }
};
