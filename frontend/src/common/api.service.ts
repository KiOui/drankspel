import axios from "axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";
import getEnvVar from "@/util/env";

class _ApiService {
  baseUri: string;

  constructor(baseUri: string) {
    this.baseUri = baseUri;
  }

  async get<T>(resource: string): Promise<AxiosResponse<T>> {
    return axios.get(`${this.baseUri}${resource}`);
  }

  async post<T>(
    resource: string,
    data: Record<string, unknown>,
  ): Promise<AxiosResponse<T>> {
    return axios.post(`${this.baseUri}${resource}`, data);
  }

  async put<T>(
    resource: string,
    data: Record<string, unknown>,
  ): Promise<AxiosResponse<T>> {
    return axios.put(`${this.baseUri}${resource}`, data);
  }

  async delete<T>(resource: string): Promise<AxiosResponse<T>> {
    return axios.delete(`${this.baseUri}${resource}`);
  }

  customRequest<T>(data: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return axios.request(data);
  }
}

const ApiService = new _ApiService(getEnvVar("VITE_APP_BACKEND_URI"));

export default ApiService;
