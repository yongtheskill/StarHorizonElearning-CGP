export default {
  responses: {},

  setResponse(id, response) {
    this.responses[id] = { id, response };
  },

  getLength() {
    return Object.keys(this.responses).length;
  },

  clearResponses() {
    this.responses = {};
  },
};
