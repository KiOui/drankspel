import ApiService from "@/common/api.service";
import type { Game } from "@/models/game.model";

class _GamesApiService {
  _apiService: typeof ApiService;

  constructor(api: typeof ApiService) {
    this._apiService = api;
  }

  getGames(): Promise<Game[]> {
    return this._apiService.get<Game[]>("/games/").then((result) => {
      return result.data;
    });
  }
}

const GamesApiService = new _GamesApiService(ApiService);

export default GamesApiService;
