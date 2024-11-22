export interface UserModel {
  name: string;
  avatarUrl: string;
}

export const emptyUser: UserModel = {
    name: "",
    avatarUrl: "",
}
