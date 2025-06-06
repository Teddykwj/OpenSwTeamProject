from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserOut, LoginRequest, ReviewOut # 사용자 관련 스키마, 리뷰 관련 스키마
from app.models import User, Review # 사용자 모델, 리뷰 모델
from app.deps import get_db # 데이터베이스 세션 의존성
from app.routers.reviews import make_review_out
from app.utils import fetch_tmdb, TMDB_API_KEY # TMDB API 키 가져오기

router = APIRouter() # 사용자 관련 라우터

# 회원가입 엔드포인트
@router.post("/register", response_model=UserOut, summary="회원가입")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.user_id == user.user_id).first(): # 이미 존재하는 user_id인지 확인
        raise HTTPException(400, "이미 존재하는 user_id")
    new_user = User(**user.dict())
    db.add(new_user) # 새 사용자 추가
    db.commit() # 데이터베이스에 커밋
    db.refresh(new_user) # 새 사용자 객체 갱신
    return new_user # 새 사용자 정보 반환
# 사용자 목록 조회 엔드포인트
@router.get("/users", response_model=List[UserOut], summary="사용자 목록 조회")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all() # 데이터베이스에서 모든 사용자 조회


# 로그인 엔드포인트
@router.post("/login", response_model=UserOut, summary="로그인")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == req.user_id).first() # user_id로 사용자 조회
    if not user or user.password != req.password: 
        raise HTTPException(400, "아이디 또는 비밀번호가 올바르지 않습니다.")
    return user

# 사용자별 리뷰 조회 엔드포인트
@router.get(
    "/users/{user_id}/reviews",
    response_model=List[ReviewOut],
    summary="사용자별 리뷰 조회"
)
def list_user_reviews( 
    user_id: str = Path(..., description="로그인 ID 문자열"),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.user_id == user_id).first() # user_id로 사용자 조회
    if not user:
        raise HTTPException(404, "해당 user_id가 없습니다.")
    db_reviews = db.query(Review).filter(Review.user_id == user.id).all() # 사용자 ID로 리뷰 조회
    return [make_review_out(r, user.user_id) for r in db_reviews]