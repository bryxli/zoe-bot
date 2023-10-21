export interface User {
  username: string;
  avatar: string;
  id: string;
}

export interface Guild {
  id: string;
  name: string;
  icon: null | string;
  owner: boolean;
  permissions: number;
  permissions_new: string;
  features: string[];
}
