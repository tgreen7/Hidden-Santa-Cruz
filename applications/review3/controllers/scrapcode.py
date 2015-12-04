__author__ = 'Thais1'

#shows boards
#{{for board in board_list:}}
#    <div class="board_n">
#        <a class="b_link" href="{{=XML(URL('default','posts',args=[board['id']]))}}" >
#        <i class="board_name">{{=board['board_name']}}</i>
#        <hr>
#        </a>
#    </div>

#{{pass}}

#  // Invent new random draft_id.
      #MAIN.set('board_id', plusone(id));

#
#       {{extend 'layout.html'}}
#
# <!--If user not logged in-->
# {{if auth.user_id is None:}}
#     <h1>{{=board['board_name']}}</h1>
#     <div class="main_login">
#         {{=A('Back to Boards', _class='btn btn-info', _href=URL('default','index'))}}
#         {{=A('Sign Up', _class='btn btn-warning', _href=URL('default', 'user', args=['register']))}}
#         {{=A('Sign In', _class='btn btn-success', _href=URL('default', 'user', args=['login']))}}
#     </div>
#     {{for post in post_list:}}
#         <div class="post_n">
#             <i class="post_name">{{=post['post_name']}}</i>
#             <div class="post_des">
#             {{if post['description']=="":}}
#                 </br>No description
#             {{else:}}
#                 </br>{{=post['description']}}
#             {{pass}}
#             </div>
#              {{if post['phone']==None:}}
#                 <div>
#                     </br>
#                 </div>
#             {{else:}}
#                 <div class="p_phone"></br>For more information call {{=post['auth_name']}} on {{=post['phone']}}</div>
#             {{pass}}
#             <div class="p_date"></br>{{=post['date_display']}}</div>
#         </div>
#     {{pass}}
#
# <!--If user logged in-->
# {{else:}}
#     <h1>{{=board['board_name']}}</h1>
#     <div class="main_login">
#         {{=A('Back to Boards', _class='btn btn-info', _href=URL('default','index'))}}
#     {{if "limit">board['counterb']:}}
#         {{=A('Create Post', _class='btn btn-primary', _href=URL('cpost',args=[board['id']], user_signature=True))}}
#     {{pass}}
#     </div>
#     {{for post in post_list:}}
#         <div class="post_n">
#             {{if auth.user_id==post['author']:}}
#                 <div class="editPencil">{{=A(I('',_class='fa fa-pencil'), _href=URL('default', 'update_post', args=[board['id'],post['id']], user_signature=True))}}
#                 {{=A(I(_class='fa fa-times'), _href=URL('default', 'delete', args=[board['id'],post['id']], user_signature=True))}}</div>
#                 <i class="post_name">{{=post['post_name']}}</i>
#         #    {{else:}}
#        #         <h2>{{=post['post_name']}}</h2>
#       #      {{pass}}
#       #      <div class="post_des">
#      #       {{if post['description']=="":}}
#      #           </br>No description
#      #       {{else:}}
#      #           </br>{{=post['description']}}
#      #       {{pass}}
#      #       </div>
#      #       {{if post['phone']==None:}}
#     #            <div>
#     #                </br>
#     #            </div>
#     #        {{else:}}
#     #            <div class="p_phone"></br>For more information call {{=post['auth_name']}} on {{=post['phone']}}</div>
#    #         {{pass}}
#   #          <div class="p_date"></br>{{=post['date_display']}}</div>
#  #       </div>
#  #    {{pass}}
#  # #{{pass}}
#  #