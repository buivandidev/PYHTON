import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import ImageModal from '../thanh_phan/ImageModal';
import { useToast } from '../thanh_phan/Toast';
import { sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import '../styles/product-detail.css';

export default function ProductDetail() {
  const { id } = useParams();
  const [sanPham, setSanPham] = useState(null);
  const [dangTai, setDangTai] = useState(true);
  const [index, setIndex] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const [extras, setExtras] = useState([]);
  const [days, setDays] = useState(1);
  const [total, setTotal] = useState(0);
  
  // State cho đánh giá
  const [danhGiaList, setDanhGiaList] = useState([]);
  const [showFormDanhGia, setShowFormDanhGia] = useState(false);
  const [formDanhGia, setFormDanhGia] = useState({ user_name: '', rating: 5, comment: '' });
  const [anhDanhGia, setAnhDanhGia] = useState(null);
  const [previewAnh, setPreviewAnh] = useState(null);
  const [dangGuiDanhGia, setDangGuiDanhGia] = useState(false);

  const navigate = useNavigate();
  const { addToast } = useToast();

  useEffect(() => {
    const layDuLieu = async () => {
      if (!id) {
        // Nếu không có ID, dùng dữ liệu demo
        setSanPham({
          id: 'demo',
          name: 'Váy Cưới Thanh Lịch',
          code: 'VD-M001',
          image_url: 'https://placehold.co/800x1100/eaeaea/333?text=Váy+Mẫu+1',
          gallery_images: [
            'https://placehold.co/800x1100/eaeaea/333?text=Váy+Mẫu+1',
            'https://placehold.co/800x1100/f7f1ea/333?text=Váy+Mẫu+2',
            'https://placehold.co/800x1100/fff0f0/333?text=Váy+Mẫu+3',
            'https://placehold.co/800x1100/e6f7f0/333?text=Váy+Mẫu+4'
          ],
          rental_price_day: 2200000,
          purchase_price: 50000000
        });
        setDangTai(false);
        return;
      }

      try {
        const res = await sanPhamAPI.layTheoId(id);
        setSanPham(res.data);
        
        // Lấy đánh giá sản phẩm
        try {
          const resDanhGia = await sanPhamAPI.layDanhGia(id);
          setDanhGiaList(resDanhGia.data || []);
        } catch (err) {
          console.log("Chưa có đánh giá");
        }
      } catch (err) {
        console.error("Lỗi tải sản phẩm:", err);
        addToast({ message: "Không tìm thấy sản phẩm", type: "error" });
      } finally {
        setDangTai(false);
      }
    };
    layDuLieu();
  }, [id]);

  useEffect(() => {
    if (sanPham) {
      setTotal(sanPham.rental_price_day * days + extras.reduce((s, e) => s + e, 0));
    }
  }, [extras, days, sanPham]);

  function toggleAccessory(el) {
    const price = Number(el.dataset.price || 0);
    const checked = el.checked;
    setExtras(prev => checked ? [...prev, price] : prev.filter(p => p !== price));
  }

  function addToCart() {
    if (!sanPham) return;
    const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
    const item = {
      id: sanPham.id,
      name: sanPham.name,
      code: sanPham.code,
      image_url: gallery[index],
      purchase_price: sanPham.purchase_price,
      rental_price_day: sanPham.rental_price_day,
      price_to_use: sanPham.purchase_price, // Giá MUA
      quantity: 1,
      loai: 'mua', // Đánh dấu là MUA
      so_luong: sanPham.so_luong // Lưu số lượng tồn kho
    };
    const existing = currentCart.findIndex(i => i.id === item.id && i.loai === 'mua');
    if (existing > -1) {
      currentCart[existing].quantity = (currentCart[existing].quantity || 1) + 1;
    } else {
      currentCart.push(item);
    }
    localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
    addToast({ message: 'Đã thêm vào giỏ hàng!', type: 'success' });
  }

  function buyNow() {
    if (!sanPham) return;
    const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
    const item = {
      id: sanPham.id,
      name: sanPham.name,
      code: sanPham.code,
      image_url: gallery[index],
      purchase_price: sanPham.purchase_price,
      rental_price_day: sanPham.rental_price_day,
      price_to_use: sanPham.purchase_price, // Giá MUA
      quantity: 1,
      loai: 'mua',
      so_luong: sanPham.so_luong // Lưu số lượng tồn kho
    };
    const existing = currentCart.findIndex(i => i.id === item.id && i.loai === 'mua');
    if (existing > -1) {
      currentCart[existing].quantity = (currentCart[existing].quantity || 1) + 1;
    } else {
      currentCart.push(item);
    }
    localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
    navigate('/gio-hang');
  }

  // Gửi đánh giá
  async function guiDanhGia(e) {
    e.preventDefault();
    if (!formDanhGia.user_name.trim()) {
      addToast({ message: 'Vui lòng nhập tên của bạn', type: 'error' });
      return;
    }
    
    setDangGuiDanhGia(true);
    try {
      const formData = new FormData();
      formData.append('user_name', formDanhGia.user_name);
      formData.append('rating', formDanhGia.rating);
      formData.append('comment', formDanhGia.comment);
      if (anhDanhGia) {
        formData.append('image', anhDanhGia);
      }
      
      await sanPhamAPI.guiDanhGia(id, formData);
      addToast({ message: 'Đánh giá đã được gửi, chờ duyệt!', type: 'success' });
      setFormDanhGia({ user_name: '', rating: 5, comment: '' });
      setAnhDanhGia(null);
      setPreviewAnh(null);
      setShowFormDanhGia(false);
    } catch (err) {
      addToast({ message: 'Lỗi gửi đánh giá', type: 'error' });
    } finally {
      setDangGuiDanhGia(false);
    }
  }

  // Xử lý chọn ảnh
  function handleChonAnh(e) {
    const file = e.target.files[0];
    if (file) {
      setAnhDanhGia(file);
      setPreviewAnh(URL.createObjectURL(file));
    }
  }

  // Tính điểm trung bình
  const diemTrungBinh = danhGiaList.length > 0 
    ? (danhGiaList.reduce((sum, dg) => sum + dg.rating, 0) / danhGiaList.length).toFixed(1)
    : 0;

  // Thống kê số sao
  const thongKeSao = [5,4,3,2,1].map(star => ({
    star,
    count: danhGiaList.filter(dg => dg.rating === star).length,
    percent: danhGiaList.length > 0 
      ? Math.round((danhGiaList.filter(dg => dg.rating === star).length / danhGiaList.length) * 100)
      : 0
  }));

  if (dangTai) return <div style={{textAlign:'center',padding:'100px'}}>Đang tải...</div>;
  if (!sanPham) return <div style={{textAlign:'center',padding:'100px'}}>Không tìm thấy sản phẩm</div>;

  // Lấy gallery images: ưu tiên gallery_images, fallback về image_url
  const gallery = Array.isArray(sanPham.gallery_images) && sanPham.gallery_images.length > 0
    ? sanPham.gallery_images
    : [sanPham.image_url];

  function next() { setIndex(i => (i + 1) % gallery.length); }
  function prev() { setIndex(i => (i - 1 + gallery.length) % gallery.length); }

  return (
    <main className="product-page">
      <div className="product-grid">
        <section className="gallery" aria-label="Hình ảnh sản phẩm">
          <div className="gallery-main">
            <button className="control-btn" onClick={prev} aria-label="Hình trước">◀</button>
            <img 
              id="mainImg" 
              src={layUrlHinhAnh(gallery[index])} 
              alt={`${sanPham.name} - ${index+1}`} 
              style={{cursor:'zoom-in'}} 
              onClick={() => setModalOpen(true)}
              onError={(e) => e.target.src = 'https://placehold.co/800x1100?text=IVIE+Studio'}
            />
            <div className="gallery-controls" aria-hidden="true">
              <button className="control-btn" onClick={() => setModalOpen(true)} title="Xem lớn">🔍</button>
            </div>
            <button className="control-btn" onClick={next} aria-label="Hình kế tiếp" style={{right:66}}>▶</button>
          </div>

          <div className="gallery-thumbs" role="tablist" aria-label="Ảnh thu nhỏ">
            {gallery.map((src,i) => (
              <div 
                key={src+i} 
                className={`thumb ${i === index ? 'active' : ''}`} 
                data-src={src} 
                tabIndex={0} 
                onClick={() => setIndex(i)} 
                onKeyDown={(e)=>{ if(e.key==='Enter') setIndex(i) }}
                style={{position:'relative'}}
              >
                <img 
                  src={layUrlHinhAnh(src)} 
                  alt={`Thumb ${i+1}`}
                  onError={(e) => e.target.src = 'https://placehold.co/160x220?text=Mẫu+'+(i+1)}
                />
                <div style={{
                  position:'absolute',
                  bottom:'8px',
                  left:'50%',
                  transform:'translateX(-50%)',
                  background:'rgba(0,0,0,0.7)',
                  color:'white',
                  padding:'4px 12px',
                  borderRadius:'12px',
                  fontSize:'0.75rem',
                  fontWeight:'600',
                  pointerEvents:'none'
                }}>
                  Mẫu {i+1}
                </div>
              </div>
            ))}
          </div>
        </section>

        <aside className="info" aria-label="Thông tin sản phẩm">
          <div className="title-row">
            <div>
              <h1 className="product-title">{sanPham.name}</h1>
              <div className="product-code">Mã: {sanPham.code}</div>
              {/* Hiển thị số lượng và trạng thái */}
              {sanPham.het_hang ? (
                <div style={{
                  display:'inline-block', background:'#d70018', color:'#fff',
                  padding:'6px 16px', borderRadius:'4px', fontWeight:'700',
                  marginTop:'8px', fontSize:'0.9rem'
                }}>
                  ❌ HẾT HÀNG
                </div>
              ) : sanPham.so_luong !== undefined && sanPham.so_luong <= 5 && (
                <div style={{
                  display:'inline-block', background:'#fef3cd', color:'#856404',
                  padding:'6px 16px', borderRadius:'4px', fontWeight:'600',
                  marginTop:'8px', fontSize:'0.85rem', border:'1px solid #ffc107'
                }}>
                  ⚠️ Chỉ còn {sanPham.so_luong} sản phẩm
                </div>
              )}
            </div>
            <div style={{textAlign:'right'}}>
              <div className="price-main">{total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'}</div>
              <div className="price-sub">Giá thuê: {sanPham.rental_price_day.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')}đ</div>
            </div>
          </div>

          <div className="options">
            <div className="option-group">
              <label className="option-label">Kích thước</label>
              <div className="sizes" role="radiogroup" aria-label="Kích thước">
                {['XS','S','M','L','XL'].map(s => (
                  <React.Fragment key={s}>
                    <input type="radio" id={`size_${s}`} name="size" value={s} defaultChecked={s==='XS'} />
                    <label className="size-btn" htmlFor={`size_${s}`}>{s}</label>
                  </React.Fragment>
                ))}
              </div>
            </div>

            <div className="option-group">
              <label className="option-label">Màu sắc</label>
              <div className="colors" role="radiogroup" aria-label="Màu sắc">
                <input type="radio" id="clr_ivory" name="color" value="ivory" defaultChecked />
                <label className="swatch" htmlFor="clr_ivory" style={{background:'#fffaf0',border:'1px solid #f1e8df'}} title="Ivory" />

                <input type="radio" id="clr_blush" name="color" value="blush" />
                <label className="swatch" htmlFor="clr_blush" style={{background:'#fff0f3'}} title="Blush" />

                <input type="radio" id="clr_pearl" name="color" value="pearl" />
                <label className="swatch" htmlFor="clr_pearl" style={{background:'#f3f9ff'}} title="Pearl" />

                <input type="radio" id="clr_champ" name="color" value="champ" />
                <label className="swatch" htmlFor="clr_champ" style={{background:'#f5eee6'}} title="Champagne" />
              </div>
            </div>

            <div style={{margin:'18px 0'}}>
              <label className="option-label">Số ngày thuê</label>
              <div style={{display:'flex',gap:8,margin:'8px 0 18px 0'}}>
                {[1,2,3,4,5,6,7].map(d=>(
                  <button
                    key={d}
                    type="button"
                    style={{
                      minWidth:36,padding:'7px 0',borderRadius:7,
                      border:days===d?'2px solid #222':'1.5px solid #bbb',
                      background:days===d?'#f5f5f5':'#fff',
                      fontWeight:days===d?700:500,cursor:'pointer',color:'#222',fontSize:'1rem'
                    }}
                    onClick={()=>setDays(d)}
                  >{d}</button>
                ))}
              </div>
            </div>
            <div className="accessories">
              <div style={{fontWeight:700,marginBottom:8,color:'var(--muted)'}}>Phụ kiện kèm theo</div>
              <table className="access" role="table" aria-label="Bảng phụ kiện">
                <tbody>
                  {[{name:'Vai nơ',price:150000},{name:'Lúp voan',price:220000},{name:'Găng tay ren',price:90000}].map(a => (
                    <tr key={a.name}>
                      <td>
                        <label>
                          <input type="checkbox" className="acc" data-price={a.price} onChange={(e)=> toggleAccessory(e.target)} /> {a.name}
                        </label>
                      </td>
                      <td className="price">{a.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="summary">Tổng hiện tại: <strong>{total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ'}</strong></div>
            </div>

            <div className="actions" role="group" aria-label="Hành động sản phẩm" style={{display:'flex', flexDirection:'column', gap:'10px'}}>
              {sanPham.het_hang ? (
                <div style={{
                  textAlign:'center', padding:'20px', background:'#f5f5f5',
                  borderRadius:'10px', color:'#666'
                }}>
                  <p style={{margin:'0 0 10px', fontWeight:'600'}}>Sản phẩm tạm hết hàng</p>
                  <p style={{margin:0, fontSize:'0.9rem'}}>Vui lòng liên hệ để được tư vấn sản phẩm tương tự</p>
                </div>
              ) : (
              <>
              <div style={{display:'flex', gap:'10px'}}>
                <button 
                  className="btn" 
                  onClick={() => addToCart()}
                  style={{
                    flex:1, padding:'14px 20px', 
                    background:'#fff', color:'#2563eb', 
                    border:'2px solid #2563eb', borderRadius:'8px',
                    fontWeight:'600', fontSize:'0.95rem', cursor:'pointer',
                    display:'flex', alignItems:'center', justifyContent:'center', gap:'8px'
                  }}
                >
                  <span style={{fontSize:'1.2rem'}}>🛒</span> Thêm vào giỏ
                </button>
                <button 
                  className="btn" 
                  onClick={() => buyNow()}
                  style={{
                    flex:1, padding:'14px 20px', 
                    background:'#f97316', color:'#fff', 
                    border:'none', borderRadius:'8px',
                    fontWeight:'600', fontSize:'0.95rem', cursor:'pointer'
                  }}
                >
                  Mua ngay
                </button>
              </div>
              <button 
                className="btn" 
                onClick={() => {
                  // Thêm vào giỏ với loại THUÊ
                  const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
                  const item = {
                    id: sanPham.id,
                    name: sanPham.name,
                    code: sanPham.code,
                    image_url: gallery[index],
                    rental_price_day: sanPham.rental_price_day,
                    price_to_use: total,
                    quantity: 1,
                    rental_days: days,
                    accessories: extras,
                    loai: 'thue', // Đánh dấu là THUÊ
                    so_luong: sanPham.so_luong // Lưu số lượng tồn kho
                  };
                  const existing = currentCart.findIndex(i => i.id === item.id && i.loai === 'thue');
                  if (existing > -1) {
                    currentCart[existing].quantity = (currentCart[existing].quantity || 1) + 1;
                    currentCart[existing].rental_days = days;
                    currentCart[existing].price_to_use = total;
                  } else {
                    currentCart.push(item);
                  }
                  localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
                  addToast({ message: 'Đã thêm vào giỏ thuê!', type: 'success' });
                  navigate('/gio-hang');
                }}
                style={{
                  width:'100%', padding:'16px 20px', 
                  background:'#3b82f6', color:'#fff', 
                  border:'none', borderRadius:'10px',
                  fontWeight:'600', fontSize:'1rem', cursor:'pointer',
                  display:'flex', flexDirection:'column', alignItems:'center', gap:'4px'
                }}
              >
                <span style={{display:'flex', alignItems:'center', gap:'8px'}}>
                  Thuê váy cưới tại IVIE <span style={{fontSize:'1.2rem'}}>›</span>
                </span>
                <span style={{fontSize:'0.8rem', fontWeight:'400', opacity:0.9}}>Thuê {days} ngày - {total.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')}đ</span>
              </button>
              </>
              )}
            </div>
          </div>

          <div className="description" aria-labelledby="descTitle">
            <h4 id="descTitle">Mô tả sản phẩm</h4>
            <p style={{margin: '0 0 8px', color: 'var(--muted)'}}>{sanPham.description || 'Một chiếc váy cưới thanh lịch, phù hợp với cả tiệc cưới ngoài trời và trong nhà.'}</p>
            <ul>
              <li>Chất liệu: {sanPham.fabric_type || 'Ren cao cấp, lót satin mịn'}</li>
              <li>Màu sắc: {sanPham.color || 'Đa dạng'}</li>
              <li>Size có sẵn: {sanPham.recommended_size || 'Đủ size'}</li>
              <li>Tông makeup: {sanPham.makeup_tone || 'Tự nhiên'}</li>
              <li>Bảo quản: Giặt khô chuyên nghiệp, bảo quản nơi khô ráo.</li>
            </ul>
          </div>
        </aside>
      </div>

      <ImageModal src={layUrlHinhAnh(gallery[index])} alt={`${sanPham.name} - ${index+1}`} open={modalOpen} onClose={() => setModalOpen(false)} />
      
      {/* Phần đánh giá sản phẩm */}
      <section className="reviews-section" style={{marginTop:'30px', padding:'24px', background:'#fff', borderRadius:'12px', border:'1px solid #eee'}}>
        <h3 style={{margin:'0 0 20px', fontFamily:'Playfair Display, serif', fontSize:'1.3rem'}}>
          Đánh giá {sanPham.name}
        </h3>
        
        {/* Thống kê đánh giá */}
        <div style={{display:'flex', gap:'40px', marginBottom:'24px', padding:'20px', background:'#fafafa', borderRadius:'10px', flexWrap:'wrap'}}>
          {/* Điểm trung bình */}
          <div style={{textAlign:'center', minWidth:'120px'}}>
            <div style={{display:'flex', alignItems:'baseline', justifyContent:'center', gap:'4px'}}>
              <span style={{fontSize:'2.5rem', fontWeight:'700', color:'#f59e0b'}}>★</span>
              <span style={{fontSize:'2.5rem', fontWeight:'700', color:'#1a1a1a'}}>{diemTrungBinh}</span>
              <span style={{fontSize:'1rem', color:'#888'}}>/5</span>
            </div>
            <div style={{color:'#666', fontSize:'0.9rem'}}>{danhGiaList.length} đánh giá</div>
          </div>
          
          {/* Biểu đồ sao */}
          <div style={{flex:1, minWidth:'200px'}}>
            {thongKeSao.map(item => (
              <div key={item.star} style={{display:'flex', alignItems:'center', gap:'8px', marginBottom:'4px'}}>
                <span style={{width:'20px', fontSize:'0.85rem'}}>{item.star}</span>
                <span style={{color:'#f59e0b'}}>★</span>
                <div style={{flex:1, height:'8px', background:'#e5e5e5', borderRadius:'4px', overflow:'hidden'}}>
                  <div style={{width:`${item.percent}%`, height:'100%', background:'linear-gradient(90deg, #22c55e, #16a34a)', borderRadius:'4px'}}></div>
                </div>
                <span style={{width:'40px', fontSize:'0.8rem', color:'#888', textAlign:'right'}}>{item.percent}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Nút viết đánh giá */}
        <div style={{display:'flex', gap:'12px', marginBottom:'24px'}}>
          <button 
            onClick={() => setShowFormDanhGia(false)}
            style={{flex:1, padding:'12px', background:'#fff', border:'1px solid #ddd', borderRadius:'25px', cursor:'pointer', fontWeight:'600'}}
          >
            Xem {danhGiaList.length} đánh giá
          </button>
          <button 
            onClick={() => setShowFormDanhGia(true)}
            style={{flex:1, padding:'12px', background:'#2563eb', color:'#fff', border:'none', borderRadius:'25px', cursor:'pointer', fontWeight:'600'}}
          >
            Viết đánh giá
          </button>
        </div>
        
        {/* Form gửi đánh giá */}
        {showFormDanhGia && (
          <form onSubmit={guiDanhGia} style={{background:'#f8fafc', padding:'24px', borderRadius:'12px', marginBottom:'24px', border:'1px solid #e2e8f0'}}>
            <h4 style={{margin:'0 0 16px', fontSize:'1.1rem'}}>Viết đánh giá của bạn</h4>
            
            <div style={{marginBottom:'16px'}}>
              <label style={{display:'block', marginBottom:'6px', fontWeight:'600', fontSize:'0.9rem'}}>Tên của bạn *</label>
              <input 
                type="text" 
                value={formDanhGia.user_name}
                onChange={(e) => setFormDanhGia({...formDanhGia, user_name: e.target.value})}
                placeholder="Nhập tên..."
                style={{width:'100%', padding:'12px', border:'1px solid #ddd', borderRadius:'8px', fontSize:'1rem'}}
              />
            </div>
            
            <div style={{marginBottom:'16px'}}>
              <label style={{display:'block', marginBottom:'6px', fontWeight:'600', fontSize:'0.9rem'}}>Đánh giá sao</label>
              <div style={{display:'flex', gap:'8px'}}>
                {[1,2,3,4,5].map(star => (
                  <span 
                    key={star}
                    onClick={() => setFormDanhGia({...formDanhGia, rating: star})}
                    style={{fontSize:'32px', cursor:'pointer', color: star <= formDanhGia.rating ? '#f59e0b' : '#ddd', transition:'transform 0.2s'}}
                    onMouseEnter={(e) => e.target.style.transform = 'scale(1.2)'}
                    onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
                  >★</span>
                ))}
                <span style={{marginLeft:'8px', color:'#666', alignSelf:'center'}}>{formDanhGia.rating}/5 sao</span>
              </div>
            </div>
            
            <div style={{marginBottom:'16px'}}>
              <label style={{display:'block', marginBottom:'6px', fontWeight:'600', fontSize:'0.9rem'}}>Nhận xét</label>
              <textarea 
                value={formDanhGia.comment}
                onChange={(e) => setFormDanhGia({...formDanhGia, comment: e.target.value})}
                placeholder="Chia sẻ trải nghiệm của bạn về sản phẩm..."
                rows={4}
                style={{width:'100%', padding:'12px', border:'1px solid #ddd', borderRadius:'8px', resize:'vertical', fontSize:'1rem'}}
              />
            </div>
            
            {/* Upload ảnh */}
            <div style={{marginBottom:'20px'}}>
              <label style={{display:'block', marginBottom:'6px', fontWeight:'600', fontSize:'0.9rem'}}>Thêm hình ảnh (tùy chọn)</label>
              <div style={{display:'flex', gap:'12px', alignItems:'flex-start', flexWrap:'wrap'}}>
                <label style={{
                  width:'100px', height:'100px', border:'2px dashed #ddd', borderRadius:'8px', 
                  display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center',
                  cursor:'pointer', background:'#fff', transition:'border-color 0.2s'
                }}
                onMouseEnter={(e) => e.currentTarget.style.borderColor = '#2563eb'}
                onMouseLeave={(e) => e.currentTarget.style.borderColor = '#ddd'}
                >
                  <span style={{fontSize:'24px', color:'#888'}}>📷</span>
                  <span style={{fontSize:'0.75rem', color:'#888', marginTop:'4px'}}>Thêm ảnh</span>
                  <input type="file" accept="image/*" onChange={handleChonAnh} style={{display:'none'}} />
                </label>
                
                {previewAnh && (
                  <div style={{position:'relative'}}>
                    <img src={previewAnh} alt="Preview" style={{width:'100px', height:'100px', objectFit:'cover', borderRadius:'8px', border:'1px solid #ddd'}} />
                    <button 
                      type="button"
                      onClick={() => { setAnhDanhGia(null); setPreviewAnh(null); }}
                      style={{position:'absolute', top:'-8px', right:'-8px', width:'24px', height:'24px', borderRadius:'50%', background:'#ef4444', color:'#fff', border:'none', cursor:'pointer', fontSize:'12px'}}
                    >✕</button>
                  </div>
                )}
              </div>
            </div>
            
            <button 
              type="submit" 
              disabled={dangGuiDanhGia}
              style={{
                padding:'14px 40px', background:'#2563eb', color:'#fff', border:'none', 
                borderRadius:'25px', cursor:'pointer', fontWeight:'600', fontSize:'1rem',
                opacity: dangGuiDanhGia ? 0.7 : 1
              }}
            >
              {dangGuiDanhGia ? 'Đang gửi...' : 'Gửi đánh giá'}
            </button>
          </form>
        )}
        
        {/* Danh sách đánh giá */}
        {!showFormDanhGia && (
          danhGiaList.length > 0 ? (
            <div style={{display:'flex', flexDirection:'column', gap:'16px'}}>
              {danhGiaList.map(dg => (
                <div key={dg.id} style={{padding:'16px', background:'#fafafa', borderRadius:'10px'}}>
                  <div style={{display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:'8px'}}>
                    <div>
                      <strong style={{fontSize:'1rem'}}>{dg.user_name}</strong>
                      <span style={{marginLeft:'8px', color:'#22c55e', fontSize:'0.85rem'}}>✓ Đã thuê tại IVIE</span>
                    </div>
                  </div>
                  <div style={{display:'flex', alignItems:'center', gap:'8px', marginBottom:'8px'}}>
                    <div style={{color:'#f59e0b'}}>
                      {'★'.repeat(dg.rating)}{'☆'.repeat(5 - dg.rating)}
                    </div>
                    <span style={{color:'#ef4444', fontSize:'0.85rem'}}>♥ Sẽ giới thiệu cho bạn bè</span>
                  </div>
                  {dg.comment && <p style={{margin:'0 0 8px', color:'#333', lineHeight:'1.5'}}>{dg.comment}</p>}
                  {dg.image_url && (
                    <img src={layUrlHinhAnh(dg.image_url)} alt="Ảnh đánh giá" style={{width:'80px', height:'80px', objectFit:'cover', borderRadius:'8px', marginTop:'8px'}} />
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p style={{textAlign:'center', color:'#999', padding:'40px'}}>Chưa có đánh giá nào. Hãy là người đầu tiên đánh giá!</p>
          )
        )}
      </section>
    </main>
  );
}
