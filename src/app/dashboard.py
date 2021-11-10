from src.infra.repositories.comment_repository import CommentRepository
from src.infra.repositories.likes_repository import LikeRepository
from src.infra.repositories.visits_repository import VisitRepository
from src.util.data_util import linear_regression, total_average


class Dashboard():
    def __init__(self, user_id):
        self.user_id = user_id
        self.comment_repository = CommentRepository(user_id=user_id)
        self.like_repository = LikeRepository(user_id=user_id)
        self.visit_repository = VisitRepository(user_id=user_id)
    
    def get_dashboard_data(self):

        comments_dict = self.comment_repository.get_comments_by_user_id()

        likes_dict = self.like_repository.get_likes_by_user_id()

        visits_dict = self.visit_repository.get_visits_by_user_id()

        comments_age_average_df = self.comment_repository.get_comments_age_average_by_user_id()
        likes_age_average_df = self.like_repository.get_likes_age_average_by_user_id()

        comments_total = self.comment_repository.total_number_of_comments()
        likes_total = self.like_repository.total_number_of_likes()
        visits_total = self.visit_repository.total_number_of_visits()

        average = total_average(comments_age_average_df, likes_age_average_df)

        linear_regression_likes = linear_regression(likes_dict)
        linear_regression_comments = linear_regression(comments_dict)
        linear_regression_visits = linear_regression(visits_dict)

        dict_merge = {'likesGrowth': likes_dict, 'commentsGrowth': comments_dict,
                      'averageUsersAge': average, 'likesPrediction': linear_regression_likes,
                      'commentsPrediction': linear_regression_comments, 'sumLikes': likes_total,
                      'sumComments': comments_total, 'visitsGrowth': visits_dict,
                      'sumVisits': visits_total, 'visitsPrediction': linear_regression_visits}

        return dict_merge
