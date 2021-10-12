import pandas as pd
from src.infra.repositories.comment_repository import CommentRepository
from src.infra.repositories.likes_repository import LikeRepository

class Dashboard():
    def __init__(self, user_id):
        self.user_id = user_id
        self.comment_repository = CommentRepository(user_id=user_id)
        self.like_repository = LikeRepository(user_id=user_id)
    
    def get_dashboard_data(self):
        comments_dict = self.comment_repository.get_comments_by_user_id()
        likes_dict = self.like_repository.get_likes_by_user_id()

        comments_age_average_df = self.comment_repository.get_comments_age_average_by_user_id()
        likes_age_average_df = self.like_repository.get_likes_age_average_by_user_id()

        df_concat = pd.concat([comments_age_average_df, likes_age_average_df])
        df_sum = df_concat['diferenca'].sum()
        count = df_concat.shape[0]

        average = int(df_sum / count)

        dict_merge = {'curtidas': likes_dict,
                  'comentarios': comments_dict, 'media': average}

        return dict_merge