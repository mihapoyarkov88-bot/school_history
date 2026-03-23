import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# HTML-код сайта (вставьте сюда ваш полный HTML-код)
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Школа №68 | Историческое наследие Уралмаша</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #f5f2eb;
            font-family: 'Inter', sans-serif;
            color: #2c2b28;
            line-height: 1.5;
        }

        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 24px;
        }

        .hero {
            background: linear-gradient(135deg, #1e3c2c 0%, #2a4a35 100%);
            color: white;
            padding: 3rem 0 2.5rem;
            border-bottom: 6px solid #c9a87b;
        }

        .hero-content {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.8rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }

        .hero p {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 700px;
        }

        .school-badge {
            display: inline-block;
            background: rgba(255,255,240,0.15);
            backdrop-filter: blur(4px);
            padding: 0.3rem 1rem;
            border-radius: 40px;
            font-size: 0.85rem;
            font-weight: 500;
            width: fit-content;
        }

        .halls-nav {
            background: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            border-bottom: 1px solid #e2ddd4;
            position: sticky;
            top: 0;
            z-index: 10;
            background: rgba(255, 253, 250, 0.98);
            backdrop-filter: blur(4px);
        }

        .tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            padding: 0.75rem 0;
        }

        .tab-btn {
            background: transparent;
            border: none;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            padding: 0.7rem 1.6rem;
            border-radius: 40px;
            cursor: pointer;
            transition: 0.2s;
            color: #4a5b4c;
            background: #f0ede7;
        }

        .tab-btn.active {
            background: #2a4a35;
            color: white;
            box-shadow: 0 2px 8px rgba(42,74,53,0.2);
        }

        .tab-btn:hover:not(.active) {
            background: #e2dbd0;
        }

        .hall {
            display: none;
            animation: fadeIn 0.3s ease;
            padding: 2.5rem 0 3.5rem;
        }

        .hall.active-hall {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px);}
            to { opacity: 1; transform: translateY(0);}
        }

        .history-grid {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .history-card {
            background: white;
            border-radius: 28px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: transform 0.2s;
            border: 1px solid #e9e2d8;
        }

        .history-card-inner {
            display: flex;
            flex-wrap: wrap;
        }

        .card-text {
            flex: 2;
            padding: 1.8rem 2rem;
        }

        .card-photo {
            flex: 1;
            min-width: 240px;
            background: #e7e2d9;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            padding: 2rem 1rem;
            border-left: 1px solid #f0e9e0;
        }

        .photo-placeholder {
            background: #cfc9be;
            width: 100%;
            max-width: 240px;
            border-radius: 20px;
            padding: 1.5rem 0.8rem;
            text-align: center;
            color: #3a3a36;
            font-weight: 500;
            box-shadow: inset 0 0 0 1px rgba(255,255,240,0.6), 0 6px 12px rgba(0,0,0,0.1);
            transition: all 0.2s;
        }

        .photo-placeholder i {
            font-size: 3rem;
            display: block;
            margin-bottom: 0.6rem;
            opacity: 0.7;
        }

        /* Стили для реального изображения */
        .actual-photo {
            width: 100%;
            max-width: 100%;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            background: #cfc9be;
        }
        
        .actual-photo img {
            width: 100%;
            height: auto;
            display: block;
            object-fit: cover;
        }
        
        .actual-photo .photo-caption {
            margin-top: 0.5rem;
            background: #2a4a35;
            display: inline-block;
            padding: 0.2rem 1rem;
            border-radius: 30px;
            color: white;
            font-size: 0.8rem;
            font-weight: 400;
            text-align: center;
            width: 100%;
        }

        .photo-caption {
            font-size: 0.8rem;
            background: #2a4a35;
            display: inline-block;
            padding: 0.2rem 1rem;
            border-radius: 30px;
            color: white;
            margin-top: 0.5rem;
            font-weight: 400;
        }

        .card-text h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.7rem;
            font-weight: 500;
            margin-bottom: 1rem;
            color: #2a4a35;
            border-left: 4px solid #c9a87b;
            padding-left: 1rem;
        }

        .card-text p {
            margin-bottom: 1rem;
            font-size: 1rem;
            color: #2e2e2c;
        }

        .date-tag {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #b47c48;
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: inline-block;
        }

        .quote-note {
            background: #faf7f0;
            border-radius: 24px;
            padding: 1.5rem;
            margin-top: 2rem;
            border-left: 6px solid #c9a87b;
            font-style: italic;
            font-size: 0.95rem;
        }

        .directors-grid {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .director-card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            border-left: 4px solid #c9a87b;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .director-period {
            font-size: 1.1rem;
            font-weight: 700;
            color: #2a4a35;
            margin-bottom: 0.5rem;
        }

        .director-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1e3c2c;
            margin-bottom: 0.75rem;
            font-family: 'Playfair Display', serif;
        }

        .director-desc {
            color: #4a5b4c;
            line-height: 1.5;
        }

        footer {
            background: #1e2c23;
            color: #cccbc6;
            text-align: center;
            padding: 2rem 0;
            font-size: 0.85rem;
            margin-top: 2rem;
        }

        @media (max-width: 780px) {
            .hero h1 { font-size: 2rem; }
            .card-text { padding: 1.5rem; }
            .card-photo { border-left: none; border-top: 1px solid #e9e2d8; }
            .history-card-inner { flex-direction: column; }
            .tabs { justify-content: center; }
            .actual-photo {
                max-width: 100%;
            }
        }

        button {
            background: none;
            border: none;
        }
    </style>
</head>
<body>

<header class="hero">
    <div class="container hero-content">
        <div class="school-badge">★  Школьный исторический музей  ★</div>
        <h1>Школа №68<br><span style="font-size: 1.8rem;">Уралмаш: вехи памяти</span></h1>
        <p>Летопись становления, подвиги учителей и судьбы учеников</p>
    </div>
</header>

<div class="halls-nav">
    <div class="container">
        <div class="tabs" id="tabsContainer">
            <button class="tab-btn active" data-hall="historyHall">📜 Зал истории</button>
            <button class="tab-btn" data-hall="futureHall">🏛️ Зал традиций (в разработке)</button>
            <button class="tab-btn" data-hall="directorsHall">👨‍🏫 Директора школы</button>
        </div>
    </div>
</div>

<main class="container">
    <div id="historyHall" class="hall active-hall">
        <div class="history-grid">
            <!-- ОБЪЕДИНЕННАЯ КАРТОЧКА: Рождение школы + Расцвет и первые педагоги -->
            <div class="history-card">
                <div class="history-card-inner">
                    <div class="card-text">
                        <span class="date-tag">✦ Декабрь 1934 – 1938 годы ✦</span>
                        <h3>Рождение первой средней школы на Уралмаше и школьный расцвет</h3>
                        <p>Комиссия приняла новое трехэтажное здание школы №145 на улице Красных партизан, 4 — первую среднюю школу на Уралмаше. Директором назначили Наталью Петровну Антонову, которая быстро сформировала сильный педагогический коллектив. Здание находилось в центре поселка, рядом с Домом культуры, что позволяло ученикам заниматься в кружках.</p>
                        <p>Уже в первые годы школа стала центром притяжения для талантливой молодежи, здесь царил дух созидания и просвещения.</p>
                        <p><strong>К 1938 году</strong> в школе обучалось уже <strong>1002 ученика</strong>. Среди первых учителей были Романычев, Жирнов, Красноперова, а также преподаватели начальных классов Дмитриева, Васильева и другие. Коллектив отличался высокой требовательностью и любовью к своему делу. В эти годы школа стала одной из самых крупных в районе, а традиции, заложенные Антоновой, оставались нерушимы.</p>
                    </div>
                    <div class="card-photo">
                        <div class="actual-photo">
                            <img src="https://i.postimg.cc/mr841yz9/izobrazenie-2026-03-22-235056287.png" alt="Фото школы">
                            <div class="photo-caption">Школа №145, историческое здание</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="history-card">
                <div class="history-card-inner">
                    <div class="card-text">
                        <span class="date-tag">✦ 1941–1949: Испытания войной ✦</span>
                        <h3>Школа №68: единство и мужество</h3>
                        <p><strong>В 1949 году</strong> школа №145 получила новый номер — <strong>68</strong>. В 1941 году из-за передачи зданий под госпитали к школе №68 присоединили учащихся и коллектив 66-й школы, объединением руководила директор Н. П. Антонова. В 1943 году, при создании Куйбышевского района и введении раздельного обучения, Антонова стала директором женской школы №67 на Эльмаше.</p>
                        <p>Школа №68 временно перешла под руководство И. В. Васильева и стала неполной мужской средней школой. Осенью 1943 года в школе работали оборонные кружки, общая успеваемость составляла 89%, а комсомольцы шефствовали над пионерами. В конце 1943 года директором назначили Е. Ф. Кулакову-Мялицину, но уже осенью 1944 года школу вновь возглавила Н. П. Антонова.</p>
                    </div>
                    <div class="card-photo">
                        <div class="photo-placeholder">
                            <i>⚔️</i>
                            <div>Оборонные кружки</div>
                            <div style="font-size:12px;">1943 год, мастерские</div>
                            <span class="photo-caption">Уроки мужества (заглушка)</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="history-card">
                <div class="history-card-inner">
                    <div class="card-text">
                        <span class="date-tag">✦ 1946 год ✦</span>
                        <h3>Переезд и возрождение на шоссе УЗТМ</h3>
                        <p>В 1946 году школа переехала в отремонтированное здание бывшего госпиталя №3750 на шоссе УЗТМ. Переезд и комплектование нового педагогического коллектива потребовали от Антоновой огромных усилий. В итоге школу №68 перевели в здание бывшей школы №77 на улице Кировградской, 40.</p>
                        <p>К 1 сентября 1946 года здесь сформировалось <strong>26 классов</strong>, а общее число учащихся достигло <strong>1365 человек</strong>. Это был рекордный набор, подтверждающий доверие семей к школе.</p>
                    </div>
                    <div class="card-photo">
                        <div class="photo-placeholder">
                            <i>🚌</i>
                            <div>Здание бывшего госпиталя</div>
                            <div style="font-size:12px;">шоссе УЗТМ / Кировградская, 40</div>
                            <span class="photo-caption">1946–1947, после ремонта</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="history-card">
                <div class="history-card-inner">
                    <div class="card-text">
                        <span class="date-tag">✦ Весна 1947 года ✦</span>
                        <h3>Завершение великой миссии Натальи Петровны</h3>
                        <p>Весной 1947 года Н. П. Антонову перевели на должность инспектора в Куйбышевский районо. На её долю выпали самые трудные годы становления школы: от нехватки учебников и программ в 30-е до объединения с другой школой и раздельного обучения в военное время. Несмотря на все тяготы и переезды, коллектив удалось сохранить, и школа осталась одной из лучших в районе.</p>
                        <p>Сегодня мы чтим её память и помним каждого педагога, кто ковал знания и характер уральских школьников.</p>
                    </div>
                    <div class="card-photo">
                        <div class="photo-placeholder">
                            <i>🏅</i>
                            <div>Наталья Петровна Антонова</div>
                            <div style="font-size:12px;">директор 1934–1943, 1944–1947</div>
                            <span class="photo-caption">Фото из архива (заглушка)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="quote-note">
            🌾 <strong>Из воспоминаний старожилов:</strong> «Школа №68 всегда была домом, где учителя становились наставниками на всю жизнь. Даже в самые суровые военные годы здесь царила дисциплина, но и теплота. Кружки, шефство, общая успеваемость 89% — показатель невероятной стойкости».
        </div>
    </div>

    <div id="futureHall" class="hall">
        <div style="background: white; border-radius: 32px; padding: 2.5rem; text-align: center; border: 1px solid #e9e2d8;">
            <h3 style="font-family: 'Playfair Display'; font-size: 2rem; color:#2a4a35;">Зал традиций</h3>
            <p style="margin: 1rem 0; font-size: 1.1rem;">Страница готовится. Здесь появятся материалы о современных достижениях, спортивных династиях и традициях школы №68.</p>
            <div class="photo-placeholder" style="margin: 1.5rem auto; max-width: 280px;">
                <i>📚✨</i>
                <div>Фотогалерея поколений (скоро)</div>
                <span class="photo-caption">ожидайте обновлений</span>
            </div>
        </div>
    </div>

    <div id="directorsHall" class="hall">
        <div style="background: white; border-radius: 32px; padding: 2rem; border: 1px solid #e9e2d8;">
            <h3 style="font-family: 'Playfair Display'; font-size: 2rem; color:#2a4a35; margin-bottom: 1.5rem;">👨‍🏫 Директора школы №68</h3>
            <div class="directors-grid">
                <div class="director-card">
                    <div class="director-period">1948–1950</div>
                    <div class="director-name">Костылев Руфим Павлович</div>
                    <div class="director-desc">Участник Великой Отечественной войны, имел боевые ранения. За два года работы проявил себя как опытный руководитель, после чего был переведён в другую школу для укрепления педагогического состава.</div>
                </div>
                <div class="director-card">
                    <div class="director-period">1955–1959</div>
                    <div class="director-name">Федотов Григорий Александрович</div>
                    <div class="director-desc">Фронтовик, награждён медалью «За отвагу». Пользовался уважением коллег и учащихся, которых называли его «Батёй». При нём школа вновь стала смешанной, усилен педагогический состав, активизирована работа пионерской и комсомольской организаций.</div>
                </div>
                <div class="director-card">
                    <div class="director-period">1959–1962</div>
                    <div class="director-name">Белкин Август Соломонович</div>
                    <div class="director-desc">Инициативный руководитель, при котором в школе появились ансамбль и радиорубка. Впоследствии — доктор педагогических наук, профессор, академик, автор более 250 научных работ.</div>
                </div>
                <div class="director-card">
                    <div class="director-period">1962–1965</div>
                    <div class="director-name">Пояркова Надежда Андреевна</div>
                    <div class="director-desc">Выдвинута на должность коллективом школы. Учитель истории, отличалась тактичностью и знанием психологии. При ней началось строительство спортивного зала.</div>
                </div>
                <div class="director-card">
                    <div class="director-period">1965–1969</div>
                    <div class="director-name">Озерская Евгения Григорьевна</div>
                    <div class="director-desc">Пережила блокаду Ленинграда. Завершила строительство спортивного зала, проявила себя как талантливый организатор. Позже избрана председателем профсоюза работников просвещения.</div>
                </div>
                <div class="director-card">
                    <div class="director-period">1969–1973</div>
                    <div class="director-name">Секисова Зоя Ильинична</div>
                    <div class="director-desc">Учитель русского языка и литературы. Ввела кабинетную систему, основала школьный музей. Создала в коллективе атмосферу взаимного уважения и доброжелательности.</div>
                </div>
            </div>
        </div>
    </div>
</main>

<footer>
    <div class="container">
        <p>МБОУ СОШ №68 | Уралмаш, историческое наследие | Все факты восстановлены из архивных документов</p>
        <p style="margin-top: 0.5rem;">★ Сайт школьного исторического проекта. Заглушки под фотографии — место для будущих экспонатов. ★</p>
    </div>
</footer>

<script>
    const tabs = document.querySelectorAll('.tab-btn');
    const halls = document.querySelectorAll('.hall');

    function switchHall(hallId) {
        halls.forEach(hall => {
            hall.classList.remove('active-hall');
        });
        const activeHall = document.getElementById(hallId);
        if(activeHall) {
            activeHall.classList.add('active-hall');
        }
        tabs.forEach(btn => {
            btn.classList.remove('active');
            if(btn.getAttribute('data-hall') === hallId) {
                btn.classList.add('active');
            }
        });
    }

    tabs.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const hallId = btn.getAttribute('data-hall');
            if(hallId) {
                switchHall(hallId);
            }
        });
    });

    const currentActiveHall = document.querySelector('.hall.active-hall');
    if(currentActiveHall && currentActiveHall.id) {
        const activeId = currentActiveHall.id;
        tabs.forEach(btn => {
            if(btn.getAttribute('data-hall') === activeId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    } else {
        switchHall('historyHall');
    }
</script>
</body>
</html>"""

def create_and_run_server():
    # Создаем папку для сайта, если её нет
    website_dir = Path("school_website")
    website_dir.mkdir(exist_ok=True)
    
    # Сохраняем HTML файл
    html_file = website_dir / "index.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    
    print(f"✅ HTML файл сохранен: {html_file.absolute()}")
    print("🚀 Запускаем веб-сервер...")
    
    # Переходим в папку с сайтом
    os.chdir(website_dir)
    
    # Создаем HTTP сервер
    PORT = 8000
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"🌐 Сервер запущен на http://localhost:{PORT}")
            print("📱 Открываем браузер...")
            
            # Открываем браузер
            webbrowser.open(f"http://localhost:{PORT}")
            
            print("🛑 Для остановки сервера нажмите Ctrl+C")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")
    except OSError:
        print(f"❌ Порт {PORT} занят. Попробуйте другой порт")
        # Альтернативный порт
        PORT = 8080
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"🌐 Сервер запущен на http://localhost:{PORT}")
            webbrowser.open(f"http://localhost:{PORT}")
            httpd.serve_forever()

if __name__ == "__main__":
    create_and_run_server()  